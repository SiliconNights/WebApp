from django.shortcuts import render, get_object_or_404
from .models import Recipe, IngredientRecipe, Ingredient, SimilarIngredient
from .forms import UploadRecipeForm
from django.shortcuts import render, redirect
import re
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
import json
from .models import Cuisine, CuisineRecipe, MealType, MealTypeRecipe

import random

# --- Helper --- #
def get_between(str, first, last):
	try:
		start = str.index(first) + len(first)
		end = str.index(last, start)
		return str[start:end]
	except ValueError:
		return ""

def get_from(str, first):
	try:
		start = str.index(first) + len(first)
		return str[start:]
	except ValueError:
		return ""

# Use for listing recipes and querying
# Generic Search
def adv_recipes_detail_list(request):
	request_url = request.build_absolute_uri()
	type = re.findall(r'\=(.*?)&', request_url)
	
	if len(type) < 3:
		return render(request, 'recipes/no_results.html')
		
	mealtypes = type[0];
	cuisines = type[1];
	ingredients = type[2];
	
	print(type)
	
	check = True
	queryset = set()
	queryset1 = set()
	queryset2 = set()
	
	
	# meal types
	typeset = set()
	mealtypes = type[0];
	mealtypes = mealtypes.replace('+', ' ')
	mealtypes = mealtypes.split('%5E')
	
	if mealtypes[0] == 'all':
		pass
		check = False
	else:
		for type in mealtypes:
			for m in MealType.objects.filter(type__icontains=type):
				typeset.add(m)
		
		for t in typeset:
			for r in MealTypeRecipe.objects.filter(type__id = t.id):
				queryset1.add(r.recipe)
	
	print('mealtypes ', len(queryset1))
	
	# cuisines
	cuisine_set = set()
	cuisines = cuisines.replace('+', ' ')
	cuisines = cuisines.split('%5E')
	
	for cuisine in cuisines:
		for c in Cuisine.objects.filter(name__icontains=cuisine):
			cuisine_set.add(c)

	for c in cuisine_set:
		for r in CuisineRecipe.objects.filter(name__id=c.id):
			queryset2.add(r.recipe)
	
	if check:
		queryset = queryset1.intersection(queryset2);
	else:
		queryset = queryset1.union(queryset2);
	
	queryset2 = set()
	ingredients = ingredients.replace('+', ' ')
	ingredients = ingredients.split('%5E')
	
	print('mealtypes + cuisine ', len(queryset))
	ingredient_set = set()
	similar_set = set()

	for q in ingredients:
		for i in Ingredient.objects.filter(name__icontains=q):
			ingredient_set.add(i)

	for i in ingredient_set:
		for s in SimilarIngredient.objects.filter(name__icontains=i.name):
			similar_set.add(s.similar)

	ingredient_set = ingredient_set.union(similar_set)

	for i in ingredient_set:
		for r in IngredientRecipe.objects.filter(ingredient=i):
			queryset2.add(r.recipe)
	
	queryset = queryset.intersection(queryset2);

	print('mealtypes + cuisine + ingredients ', len(queryset))
	context = {'object_list': queryset,}

	return render(request, 'recipes/list_results.html', context)



# Use for listing recipes and querying
# Generic Search
def recipes_detail_list(request):
	request_url = request.build_absolute_uri()
	type = re.findall(r'\?(.*?)\=', request_url)


	queryset = set()
	if type[0] == 'all':
		query = request.GET['all']
		queryset = search_by_recipe_name(query)

	elif type[0] == 'recipe':
		query = request.GET['recipe']
		queryset = search_by_recipe_name(query)


	# Needs to be refined returning ingredients and recipes as results
	elif type[0] == 'ingredients':
		query = request.GET['ingredients']
		queryset = search_by_ingredient(query)

	elif type[0] == 'cuisine':
		query = request.GET['cuisine']
		queryset = search_by_cuisine(query)

	elif type[0] == 'meal+type':
		query = request.GET['meal type']
		queryset = search_by_type(query)

	if len(queryset) == 0:
		return render(request, 'recipes/no_results.html')

	number_of_pages = 1
	page_list = []
	if len(queryset) > 12:
		number_of_pages = (len(queryset) // 12) + 1
		page_list = [x+1 for x in range(number_of_pages)]


	context = {'object_list': queryset,}

	return render(request, 'recipes/list_results.html', context)

def search_by_type(query):
	if len(query) == 0:
		return set()

	queryset = set()
	typeset = set()
	
	for m in MealType.objects.filter(type__icontains=query):
		typeset.add(m)
	
	for t in typeset:
		for r in MealTypeRecipe.objects.filter(type__id = t.id):
			queryset.add(r.recipe)
	return queryset

def search_by_cuisine(list_of_queries):
	list_of_queries = parse_query(list_of_queries)
	
	if len(list_of_queries) == 0:
		return set()


	query_set = set()
	cuisine_set = set()
	
	for q in list_of_queries:
		print(q)
		for c in Cuisine.objects.filter(name__icontains=q):
			cuisine_set.add(c)


	for c in cuisine_set:
		for r in CuisineRecipe.objects.filter(name__id=c.id):
			query_set.add(r.recipe)

	return query_set

def search_by_ingredient(list_of_queries):
	list_of_queries = parse_query(list_of_queries)
	
	all_ing = Ingredient.objects.all()
	for i in range(5):
		print (all_ing[random.randint(0, len(all_ing)-1)].name)

	if len(list_of_queries) == 0:
		return set()

	query_set = set()
	ingredient_set = set()
	similar_set = set()

	for q in list_of_queries:
		for i in Ingredient.objects.filter(name__icontains=q):
			ingredient_set.add(i)

	for i in ingredient_set:
		for s in SimilarIngredient.objects.filter(name__icontains=i.name):
			similar_set.add(s.similar)

	ingredient_set = ingredient_set.union(similar_set)

	for i in ingredient_set:
		for r in IngredientRecipe.objects.filter(ingredient=i):
			query_set.add(r.recipe)

	return query_set

# Supports advanced search functionality
def advanced_search(request):
	return render(request, 'recipes/advanced_search.html')

def generic_search(query):
	if len(query) == 0:
		return set()

	# Contains all the queries in a generic search
	list_of_queries = parse_query(query)

	queryset = set()

	queryset = queryset.union(search_by_recipe_name(list_of_queries))

	ingredient_set = set()

	ingredient_set = ingredient_set.union(search_by_ingredient_name(list_of_queries))

	ingredient_set = search_similar_ingredients(ingredient_set, list_of_queries)

	queryset = queryset.union(search_ingredient_recipe(ingredient_set))
	
	queryset = queryset.union(search_by_cuisine(ingredient_set))
	
	queryset = queryset.union(search_by_type(ingredient_set))

	return queryset

# Parse a query represented as a string
def parse_query(query):
	query_list = re.split(r'[^a-zA-Z]', query)

	query_list = list(filter(lambda a: a != '', query_list))

	if len(query_list) > 1:
		combined_list_as_string = []
		for q in query_list:
			combined_list_as_string.append(q)
			combined_list_as_string.append(' ')
		else:
			del combined_list_as_string[-1]


		query_list.append(''.join(combined_list_as_string))


	return query_list

def search_by_recipe_name(list_of_queries):
	if (len(list_of_queries) == 0):
		return set()

	queryset = set()
	for recipe in Recipe.objects.filter(name__icontains=list_of_queries):
		queryset.add(recipe)
	return queryset

def search_ingredient_recipe(ingredient_set):
	queryset = set()

	# Adds the remaining results from IngredientRecipe into queryset
	for i in ingredient_set:
		for recipe in IngredientRecipe.objects.filter(ingredient=i):
			queryset.add(recipe.recipe)

	return queryset

def search_by_ingredient_name(list_of_queries):
	queryset = set()
	ingredient_set = set()
	for q in list_of_queries:
		# Search By Ingredient Name In Ingredient Table
		for i in Ingredient.objects.filter(name__icontains=q):
			ingredient_set.add(i)

	similar_ingredients = set()
	for i in ingredient_set:
		for s in SimilarIngredient.objects.filter(name__icontains=i.name):
			similar_ingredients.add(i)

	ingredient_set = ingredient_set.union(similar_ingredients)

	for i in ingredient_set:
		for r in IngredientRecipe.objects.filter(ingredient=i):
			queryset.add(r)

	return ingredient_set

def search_similar_ingredients(ingredients, list_of_queries):
	ingredient_set = set()
	similar_ingredient_set = set()

	# Finds Similar Ingredients
	for q in list_of_queries:
		for items in SimilarIngredient.objects.filter(name__icontains=q):
			ingredient_set.add(items.similar)

	for i in ingredients:
		for items in SimilarIngredient.objects.filter(name__icontains=i.name):
			similar_ingredient_set.add(items.similar)

	return ingredient_set.union(similar_ingredient_set)



def recipes_detail_display(request, pk):
	recipe = Recipe.objects.get(pk=pk)

	# Wikimedia Recipes
	if recipe.author == 'wikimedia':

		ingredients = recipe.ingredients.strip('\n')
		headers = re.findall(r'(\=\=\=.*?\=\=\=)', ingredients)

		# Get ingredient sections
		ingredients_sections = []
		ingredients_header = []
		ingredients_body = []

		if len(headers) > 0:

			if ingredients.index(headers[0]) != 0:
				headers.insert(0, 'none')
				ingredients_header.append('none')

			for i in range(0, len(headers)):
				if i == 0 and headers[i] == 'none':
						section_ingredients = ingredients[0:ingredients.index(headers[1])].strip('\n')
						list = section_ingredients.split('\n')
						ingredients_body.append(list)

				elif i == 0:
						section_ingredients = get_between(ingredients, headers[0], headers[1]).strip('\n')
						ingredients_header.append(headers[0])
						list = section_ingredients.split('\n')
						ingredients_body.append(list)

				elif i < len(headers) - 1:
					section_ingredients = get_between(ingredients, headers[i], headers[i+1]).strip('\n')
					ingredients_header.append(headers[i])
					list = section_ingredients.split('\n')
					ingredients_body.append(list)

				elif i == len(headers) - 1:
					section_ingredients = get_from(ingredients, headers[i]).strip('\n')
					ingredients_header.append(headers[i])
					list = section_ingredients.split('\n')
					ingredients_body.append(list)


			ingredients_header = [item.strip('=') for item in ingredients_header]
			ingredients_sections = zip(ingredients_header, ingredients_body)


		else:
			ingredients_header.append('none')
			list = ingredients.split('\n')
			ingredients_body.append(list)
			ingredients_sections = zip(ingredients_header, ingredients_body)



		instructions = recipe.instructions.strip('\n')
		headers = re.findall(r'(\=\=\=.*?\=\=\=)', instructions)

		# Get instruction sections
		instructions_sections = []
		instructions_header = []
		instructions_body = []
		if len(headers) > 0:

			if instructions.index(headers[0]) != 0:
				headers.insert(0, 'none')
				instructions_header.append('none')

			for i in range(0, len(headers)):
				if i == 0 and headers[i] == 'none':
						section_instructions = instructions[0:instructions.index(headers[1])].strip('\n')
						list = section_instructions.split('\n')
						instructions_body.append(list)

				elif i == 0:
						section_instructions = get_between(instructions, headers[0], headers[1]).strip('\n')
						instructions_header.append(headers[0])
						list = section_instructions.split('\n')
						instructions_body.append(list)

				elif i < len(headers) - 1:
					section_instructions = get_between(instructions, headers[i], headers[i+1]).strip('\n')
					instructions_header.append(headers[i])
					list = section_instructions.split('\n')
					instructions_body.append(list)

				elif i == len(headers) - 1:
					section_instructions = get_from(instructions, headers[i]).strip('\n')
					instructions_header.append(headers[i])
					list = section_instructions.split('\n')
					instructions_body.append(list)


			instructions_header = [item.strip('=') for item in instructions_header]
			instructions_sections = zip(instructions_header, instructions_body)

		else:
			instructions_header.append('none')
			list = instructions.split('\n')
			instructions_body.append(list)
			instructions_sections = zip(instructions_header, instructions_body)




	# Uploaded recipes
	else:
		# Get ingredient sections
		ingredients_sections = []
		ingredients_header = []
		ingredients_body = []

		ingredients = recipe.ingredients.strip('\n')

		ingredients_header.append('none')
		list = ingredients.split('\n')
		ingredients_body.append(list)
		ingredients_sections = zip(ingredients_header, ingredients_body)


		# Get instruction sections
		instructions_sections = []
		instructions_header = []
		instructions_body = []

		instructions = recipe.instructions.strip('\n')

		instructions_header.append('none')
		list = instructions.split('\n')
		instructions_body.append(list)
		instructions_sections = zip(instructions_header, instructions_body)

	description = recipe.description.strip();
	mealtype = recipe.type.strip().title();
	cuisine = recipe.cuisine.strip().title();

	args = {'recipe': recipe,
				'ingredients_sections': ingredients_sections,
				'instructions_sections': instructions_sections,
				'description': description,
				'mealtype' : mealtype,
				'cuisine' : cuisine,
				}
	return render(request, 'recipes/recipe_page.html', args)

def upload_recipe(request):

	if request.user.is_authenticated:
		if request.method == 'POST':
			form = UploadRecipeForm(request.POST, request.FILES or None)
			if form.is_valid():
				form.instance.user = request.user
				form.save()
				return redirect('/recipes/recipe_uploaded')
		else:
			form = UploadRecipeForm()
		return render(request,'recipes/uploadRecipe.html',{'form':form})
	else:
		return redirect('/accounts/login')

def uploaded_recipe(request):
	return render(request, 'recipes/uploaded.html', )



##	  if request.method == 'POST':
##
##		  imageForm = ImageUpload(request.POST, request.FILES)
##
##
##		  if imageForm.is_valid():
##
##			  image = Image(image = request.FILES['image'])
##			  #Image.image = ImageUpload.cleaned_data["image"]
##			  Image.save()
##
##
##			  return HttpResponseRedirect(reverse(''))
##
##	  else:
##		  imageForm = ImageUpload()
##
##	  return render(request,'recipes/uploadRecipe.html',{'imageForm':imageForm})
def get_recipes(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		recipes = Recipe.objects.filter(name__icontains=q)
		results = []

		for re in recipes:
			recipe_json = {}
			recipe_json = re.name
			results.append(recipe_json)
			data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)
