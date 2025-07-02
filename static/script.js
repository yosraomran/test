document.addEventListener('DOMContentLoaded', () => {
    const productListDiv = document.querySelector('.product-list');
    const productSelect = document.getElementById('product');
    const orderForm = document.getElementById('orderForm');
    const contactForm = document.getElementById('contactForm');

    // Function to fetch and display products
    const fetchProducts = async () => {
        try {
            const response = await fetch('/api/products');
            const products = await response.json();

            if (productListDiv) {
                productListDiv.innerHTML = ''; // Clear existing products
                products.forEach(product => {
                    const productItem = document.createElement('div');
                    productItem.classList.add('product-item');
                    productItem.innerHTML = `
                        <img src="${product.image_url || 'placeholder.jpg'}" alt="${product.name}">
                        <h3>${product.name}</h3>
                        <p>${product.description || ''}</p>
                        <p class="price">$${product.price.toFixed(2)}</p>
                    `;
                    productListDiv.appendChild(productItem);
                });
            }

            if (productSelect) {
                productSelect.innerHTML = '<option value="">-- Select a Product --</option>'; // Clear and add default
                products.forEach(product => {
                    const option = document.createElement('option');
                    option.value = product.id;
                    option.textContent = `${product.name} - $${product.price.toFixed(2)}`;
                    productSelect.appendChild(option);
                });
            }

        } catch (error) {
            console.error('Error fetching products:', error);
            if (productListDiv) productListDiv.innerHTML = '<p>Error loading products.</p>';
            if (productSelect) productSelect.innerHTML = '<option value="">Error loading products</option>';
        }
    };

    // Fetch products when the page loads if a product list or select exists
    if (productListDiv || productSelect) {
        fetchProducts();
    }

    // Handle order form submission
    if (orderForm) {
        orderForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(orderForm);
            const orderData = {
                product_id: parseInt(formData.get('product')),
                quantity: parseInt(formData.get('quantity')),
                customer_name: formData.get('name'),
                customer_email: formData.get('email'),
                shipping_address: formData.get('address'),
            };

            try {
                const response = await fetch('/api/orders/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(orderData),
                });

                if (response.ok) {
                    alert('Order placed successfully!');
                    orderForm.reset();
                } else {
                    const errorData = await response.json();
                    alert(`Failed to place order: ${errorData.detail || response.statusText}`);
                }
            } catch (error) {
                console.error('Error placing order:', error);
                alert('An error occurred while placing your order.');
            }
        });
    }

    // Handle contact form submission (basic example)
    if (contactForm) {
        contactForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(contactForm);
            const contactData = {
                name: formData.get('name'),
                email: formData.get('email'),
                subject: formData.get('subject'),
                message: formData.get('message'),
            };

            // In a real application, you would send this data to your backend
            console.log('Contact form submitted:', contactData);
            alert('Thank you for your message! We will get back to you shortly.');
            contactForm.reset();

            // Example of sending to a backend endpoint (you would need to create this)
            /*
            try {
                const response = await fetch('/api/contact/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(contactData),
                });

                if (response.ok) {
                    alert('Thank you for your message! We will get back to you shortly.');
                    contactForm.reset();
                } else {
                    const errorData = await response.json();
                    alert(`Failed to send message: ${errorData.detail || response.statusText}`);
                }
            } catch (error) {
                console.error('Error sending contact message:', error);
                alert('An error occurred while sending your message.');
            }
            */
        });
    }
});
