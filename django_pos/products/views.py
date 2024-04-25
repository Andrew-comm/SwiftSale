from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Category, Product,SubCategory


@login_required(login_url="/accounts/login/")
def categories_list_view(request):
    context = {
        "active_icon": "products_categories",
        "categories": Category.objects.all()
    }
    return render(request, "products/categories.html", context=context)


@login_required(login_url="/accounts/login/")
def categories_add_view(request):
    context = {
        "active_icon": "products_categories",
        "category_status": Category.status.field.choices
    }

    if request.method == 'POST':
        # Save the POST arguments
        data = request.POST

        attributes = {
            "name": data['name'],
            "status": data['state'],
            "description": data['description']
        }

        # Check if a category with the same attributes exists
        if Category.objects.filter(**attributes).exists():
            messages.error(request, 'Category already exists!',
                           extra_tags="warning")
            return redirect('products:categories_add')

        try:
            # Create the category
            new_category = Category.objects.create(**attributes)

            # If it doesn't exist, save it
            new_category.save()

            messages.success(request, 'Category: ' +
                             attributes["name"] + ' created successfully!', extra_tags="success")
            return redirect('products:categories_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('products:categories_add')

    return render(request, "products/categories_add.html", context=context)


@login_required(login_url="/accounts/login/")
def categories_update_view(request, category_id):
    """
    Args:
        request:
        category_id : The category's ID that will be updated
    """

    # Get the category
    try:
        # Get the category to update
        category = Category.objects.get(id=category_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the category!', extra_tags="danger")
        print(e)
        return redirect('products:categories_list')

    context = {
        "active_icon": "products_categories",
        "category_status": Category.status.field.choices,
        "category": category
    }

    if request.method == 'POST':
        try:
            # Save the POST arguments
            data = request.POST

            attributes = {
                "name": data['name'],
                "status": data['state'],
                "description": data['description']
            }

            # Check if a category with the same attributes exists
            if Category.objects.filter(**attributes).exists():
                messages.error(request, 'Category already exists!',
                               extra_tags="warning")
                return redirect('products:categories_add')

            # Get the category to update
            category = Category.objects.filter(
                id=category_id).update(**attributes)

            category = Category.objects.get(id=category_id)

            messages.success(request, '¡Category: ' + category.name +
                             ' updated successfully!', extra_tags="success")
            return redirect('products:categories_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the elimination!', extra_tags="danger")
            print(e)
            return redirect('products:categories_list')

    return render(request, "products/categories_update.html", context=context)


@login_required(login_url="/accounts/login/")
def categories_delete_view(request, category_id):
    """
    Args:
        request:
        category_id : The category's ID that will be deleted
    """
    try:
        # Get the category to delete
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, '¡Category: ' + category.name +
                         ' deleted!', extra_tags="success")
        return redirect('products:categories_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('products:categories_list')
    
    #subcategories
@login_required(login_url="/accounts/login/")
def subcategories_list_view(request):
    context = {
        "active_icon": "products_categories",
        "subcategories": SubCategory.objects.all()
    }
    return render(request, "products/subcategories.html", context=context)


@login_required(login_url="/accounts/login/")
def subcategories_add_view(request):
    context = {
        "active_icon": "products_categories",
    }

    if request.method == 'POST':
        data = request.POST

        category_id = data['category']

        try:
            category = Category.objects.get(id=category_id)

            subcategory = SubCategory.objects.create(
                category=category,
                name=data['name']
            )

            subcategory.save()

            messages.success(request, 'Subcategory: ' +
                             subcategory.name + ' created successfully!', extra_tags="success")
            return redirect('products:subcategories_list')
        except Exception as e:
            messages.error(request, 'There was an error during the creation!',
                           extra_tags="danger")
            print(e)
            return redirect('products:subcategories_add')

    return render(request, "products/subcategories_add.html", context=context)


@login_required(login_url="/accounts/login/")
def subcategories_update_view(request, subcategory_id):
    try:
        subcategory = SubCategory.objects.get(id=subcategory_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the subcategory!', extra_tags="danger")
        print(e)
        return redirect('products:subcategories_list')

    context = {
        "active_icon": "products_categories",
        "subcategory": subcategory
    }

    if request.method == 'POST':
        try:
            data = request.POST

            subcategory.name = data['name']
            subcategory.save()

            messages.success(request, '¡Subcategory: ' + subcategory.name +
                             ' updated successfully!', extra_tags="success")
            return redirect('products:subcategories_list')
        except Exception as e:
            messages.error(
                request, 'There was an error during the update!', extra_tags="danger")
            print(e)
            return redirect('products:subcategories_list')

    return render(request, "products/subcategories_update.html", context=context)


@login_required(login_url="/accounts/login/")
def subcategories_delete_view(request, subcategory_id):
    try:
        subcategory = SubCategory.objects.get(id=subcategory_id)
        subcategory.delete()
        messages.success(request, '¡Subcategory: ' + subcategory.name +
                         ' deleted!', extra_tags="success")
        return redirect('products:subcategories_list')
    except Exception as e:
        messages.error(
            request, 'There was an error during the deletion!', extra_tags="danger")
        print(e)
        return redirect('products:subcategories_list')


@login_required(login_url="/accounts/login/")
def products_list_view(request):
    if request.method == "POST" and "sale" in request.POST:
        product_id = request.POST.get("product_id")
        quantity_sold = int(request.POST.get("quantity_sold"))
        product = Product.objects.get(id=product_id)
        if product.stock >= quantity_sold:
            # Update product stock
            product.stock -= quantity_sold
            product.save()
            # Here you might want to add additional logic for sales recording, such as updating total sales, etc.
        else:
            # Handle insufficient stock situation, you can redirect or render an error message
            return render(request, "error.html", {"message": "Insufficient stock!"})
        return redirect("products_list")  # Redirect back to the products list page
    else:
        products = Product.objects.all()
        context = {
            "active_icon": "products",
            "products": products
        }
        return render(request, "products/products.html", context=context)



@login_required(login_url="/accounts/login/")
def products_add_view(request):
    categories = Category.objects.filter(status="ACTIVE").prefetch_related('subcategories')  # Fetch categories with subcategories
    context = {
        "active_icon": "products_categories",
        "product_status": Product.STATUS_CHOICES,
        "categories": categories
    }

    if request.method == 'POST':
        # Save the POST arguments
        data = request.POST

        category_id = data['category']
        subcategory_id = data['subcategory']

        attributes = {
            "name": data['name'],
            "status": data['state'],
            "description": data['description'],
            "category": Category.objects.get(id=category_id),
            "price": data['price']
        }

        if subcategory_id:
            attributes['subcategory'] = SubCategory.objects.get(id=subcategory_id)

        # Check if a product with the same attributes exists
        if Product.objects.filter(**attributes).exists():
            messages.error(request, 'Product already exists!', extra_tags="warning")
            return redirect('products:products_add')

        try:
            # Create the product
            new_product = Product.objects.create(**attributes)

            messages.success(request, 'Product: ' + attributes["name"] + ' created successfully!', extra_tags="success")
            return redirect('products:products_list')
        except Exception as e:
            messages.success(request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('products:products_add')

    return render(request, "products/products_add.html", context=context)


@login_required(login_url="/accounts/login/")
def products_update_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Exception as e:
        messages.success(request, 'There was an error trying to get the product!', extra_tags="danger")
        print(e)
        return redirect('products:products_list')

    categories = Category.objects.all().prefetch_related('subcategories')
    context = {
        "active_icon": "products",
        "product_status": Product.STATUS_CHOICES,
        "product": product,
        "categories": categories
    }

    if request.method == 'POST':
        try:
            data = request.POST
            category_id = data['category']
            subcategory_id = data['subcategory']

            attributes = {
                "name": data['name'],
                "status": data['state'],
                "description": data['description'],
                "category": Category.objects.get(id=category_id),
                "price": data['price']
            }

            if subcategory_id:
                attributes['subcategory'] = SubCategory.objects.get(id=subcategory_id)

            if Product.objects.filter(**attributes).exclude(id=product_id).exists():
                messages.error(request, 'Product already exists!', extra_tags="warning")
                return redirect('products:products_add')

            Product.objects.filter(id=product_id).update(**attributes)

            messages.success(request, 'Product: ' + product.name + ' updated successfully!', extra_tags="success")
            return redirect('products:products_list')
        except Exception as e:
            messages.success(request, 'There was an error during the update!', extra_tags="danger")
            print(e)
            return redirect('products:products_list')

    return render(request, "products/products_update.html", context=context)

@login_required(login_url="/accounts/login/")
def products_delete_view(request, product_id):
    """
    Args:
        request:
        product_id : The product's ID that will be deleted
    """
    try:
        # Get the product to delete
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, '¡Product: ' + product.name +
                         ' deleted!', extra_tags="success")
        return redirect('products:products_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('products:products_list')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/accounts/login/")
def get_products_ajax_view(request):
    if request.method == 'POST':
        if is_ajax(request=request):
            data = []

            products = Product.objects.filter(
                name__icontains=request.POST['term'])
            for product in products[0:10]:
                item = product.to_json()
                data.append(item)

            return JsonResponse(data, safe=False)
