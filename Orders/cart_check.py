from .models import Cart
import uuid

def createCartForAnonymousUser(request):
    request.session['nonuser'] = str(uuid.uuid4())
    cart = Cart.objects.create(session_id=request.session['nonuser'])
    return cart    