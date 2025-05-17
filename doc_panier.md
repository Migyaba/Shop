# 📄 Documentation — Gestion du panier avec Django & AJAX

## 1. Bouton "Ajouter au panier"

Dans chaque template où tu affiches un produit (exemple : `index.html`) :

```django-html
<button id="{{product.id}}" class="btn addp btn-primary">Ajouter au panier</button>
```
- L’attribut `id` contient l’identifiant du produit.
- La classe `addp` permet de cibler le bouton en JavaScript.

---

## 2. Icône panier dans la navbar

Dans `base.html`, ajoute à la fin de la barre de navigation :

```django-html
<ul class="navbar-nav ms-auto">
  <li class="nav-item">
    <a class="nav-link position-relative" href="#">
      <i class="bi bi-cart" style="font-size: 1.5rem;"></i>
      <sup id="cart-total" style="font-size: 1rem; color: #dc3545;">0 FCFA</sup>
    </a>
  </li>
</ul>
```
- Le montant total du panier s’affiche dans `<sup id="cart-total">`.

---

## 3. Script JavaScript global (`base.html`)

Dans le bloc `{% block scripts %}` de `base.html` :

```html
{% block scripts %}
<script>
function updateCartTotal() {
    $.ajax({
        url: "{% url 'cart_total' %}",
        method: "GET",
        success: function(response) {
            $('#cart-total').text(response.total + ' FCFA');
        }
    });
}

$(document).ready(function() {
    updateCartTotal();
});

$(document).on('click', '.addp', function() {
    var productId = this.id.toString();
    $.ajax({
        url: "{% url 'add_to_cart' %}",
        method: "POST",
        data: {
            'product_id': productId,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        success: function(response) {
            alert('Produit ajouté au panier !');
            updateCartTotal();
        },
        error: function() {
            alert('Erreur lors de l\'ajout au panier.');
        }
    });
});
</script>
{% endblock %}
```
- Ce script gère l’ajout au panier et la mise à jour du montant total sans recharger la page.

---

## 4. Vue Django pour l’ajout au panier

Dans `views.py` :

```python
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        request.session['cart'] = cart
        return JsonResponse({'message': 'Produit ajouté au panier'})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=400)
```
- Ajoute ou incrémente le produit dans le panier stocké en session.

---

## 5. Vue Django pour le montant total

Toujours dans `views.py` :

```python
from django.views.decorators.http import require_GET

@require_GET
def cart_total(request):
    cart = request.session.get('cart', {})
    total = 0
    for pid, qty in cart.items():
        try:
            product = Product.objects.get(pk=pid)
            total += product.price * qty
        except Product.DoesNotExist:
            continue
    return JsonResponse({'total': total})
```
- Calcule le montant total du panier et le retourne en JSON.

---

## 6. URLs à ajouter

Dans `urls.py` :

```python
path('ajouter-au-panier/', add_to_cart, name='add_to_cart'),
path('cart-total/', cart_total, name='cart_total'),
```

---

## 7. Dépendances

Dans le `<head>` de `base.html` :

```html
<script src="https://code.jquery.com/jquery-3.7.1.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
```

---

## Fonctionnement global

1. L’utilisateur clique sur "Ajouter au panier".
2. Un appel AJAX ajoute le produit côté serveur (session Django).
3. Le montant total du panier est recalculé et affiché dynamiquement à côté de l’icône panier.
4. Une alerte confirme l’ajout.

---

**Remarque :**  
Tout le code JavaScript doit être centralisé dans `base.html` pour fonctionner sur toutes les pages héritées.

---

N’hésite pas à copier/coller ce texte dans un fichier `README.md` ou `doc_panier.md` pour ton projet !