from django.shortcuts import render,get_object_or_404,redirect
from suppliers.models import Order  # Import the Order model from supplier app
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from .form import CustomerProfileForm
from suppliers.models import Order, Rating ,Suppliers
from django.contrib import messages
# Create your views here.
@login_required
def customer_orders(request):
    # Check if the customer has already rated the supplier for each order
    ratings = Rating.objects.filter(
        customer=request.user,
        supplier=OuterRef('supplier')
    )
    
    orders = Order.objects.filter(customer_name=request.user).annotate(
        rating_exists=Exists(ratings)
    ).order_by('-created_at')
    
    return render(request, 'customer/customer_orders.html', {'orders': orders})
def rate_supplier(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer_name=request.user)

    # Only allow rating if delivered
    if order.status != 'Delivered':
        return redirect('customer_orders')

    # Check if already rated
    existing_rating = Rating.objects.filter(customer=request.user, supplier=order.supplier).first()
    if existing_rating:
        return redirect('customer_orders')

    if request.method == 'POST':
        rating_value = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '').strip()

        if rating_value < 1 or rating_value > 5:
            error = "Rating must be between 1 and 5."
            return render(request, 'customer/rate_supplier.html', {'order': order, 'error': error})

        Rating.objects.create(
            customer=request.user,
            supplier=order.supplier,
            rating=rating_value,
            comment=comment
        )
        return redirect('customer_orders')

    return render(request, 'customer/rate_supplier.html', {'order': order})


def nearby_suppliers(request):
    profile = request.user.customerProfile

    suppliers = Suppliers.objects.filter(
        location__icontains=profile.area
    )

    return render(request, 'customer/nearby_suppliers.html', {
        'suppliers': suppliers
    })

@login_required
def edit_profile(request):
    profile = request.user.customerprofile

    if request.method == "POST":
        form = CustomerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("edit_profile")
    else:
        form = CustomerProfileForm(instance=profile)

    return render(request, "customer/edit_profile.html", {"form": form})

