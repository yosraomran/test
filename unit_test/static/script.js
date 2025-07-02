import { JSDOM } from 'jsdom';
import fetchMock from 'jest-fetch-mock';
const sinon = require('sinon');
import { render, fireEvent, waitFor } from '@testing-library/dom';
import { faker } from '@faker-js/faker';
import orderFormHtml from './orderFormHtml'; // Assume you have a file with the HTML

describe('fetchProducts function', () => {
  beforeEach(() => {
    document.body.innerHTML = '<div class="product-list"></div><select id="product"></select>';
  });

  afterEach(() => {
    fetchMock.resetMocks();
  });

  it('should fetch products and display them', async () => {
    const products = [
      { id: 1, name: 'Product 1', image_url: 'image1.jpg', description: 'Desc 1', price: 10.99 },
      { id: 2, name: 'Product 2', image_url: 'image2.jpg', description: 'Desc 2', price: 5.99 },
    ];

    fetchMock.mockResponseOnce(JSON.stringify(products));

    await fetchProducts();

    await waitFor(() => {
      expect(document.querySelectorAll('.product-item')).toHaveLength(2);
    });

    expect(document.querySelector('.product-item img').src).toContain('image1.jpg');
    expect(document.querySelector('.product-item h3').textContent).toBe('Product 1');
    expect(document.querySelector('.product-item .price').textContent).toBe('$10.99');

    expect(document.getElementById('product').options).toHaveLength(3); // 1 default + 2 products
  });

  it('should handle fetch error', async () => {
    fetchMock.mockRejectOnce(new Error('Network error'));

    await fetchProducts();

    await waitFor(() => {
      expect(document.querySelector('.product-list')).toHaveTextContent('Error loading products.');
    });

    expect(document.getElementById('product').innerHTML).toContain('Error loading products');
  });

  it('should handle empty product list', async () => {
    fetchMock.mockResponseOnce(JSON.stringify([]));

    await fetchProducts();

    await waitFor(() => {
      expect(document.querySelector('.product-list')).toHaveTextContent('');
    });

    expect(document.getElementById('product').options).toHaveLength(1); // Only default option
  });
});

describe('orderForm submission', () => {
  beforeEach(() => {
    document.body.innerHTML = orderFormHtml;
  });

  afterEach(() => {
    fetchMock.resetMocks();
  });

  it('should submit order successfully', async () => {
    const orderData = {
      product_id: 1,
      quantity: 2,
      customer_name: faker.name.fullName(),
      customer_email: faker.internet.email(),
      shipping_address: faker.address.streetAddress(),
    };

    fetchMock.mockResponseOnce(JSON.stringify({}));

    const { getByLabelText, getByText } = render(document.body.innerHTML);

    fireEvent.change(getByLabelText('Product:'), { target: { value: orderData.product_id } });
    fireEvent.change(getByLabelText('Quantity:'), { target: { value: orderData.quantity } });
    fireEvent.change(getByLabelText('Name:'), { target: { value: orderData.customer_name } });
    fireEvent.change(getByLabelText('Email:'), { target: { value: orderData.customer_email } });
    fireEvent.change(getByLabelText('Shipping Address:'), { target: { value: orderData.shipping_address } });

    fireEvent.click(getByText('Place Order'));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledTimes(1);
      expect(fetch).toHaveBeenCalledWith('/api/orders/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData),
      });
    });

    expect(getByText('Order placed successfully!')).toBeInTheDocument();
  });

  it('should handle order submission error', async () => {
    const errorData = { detail: 'Product out of stock' };
    fetchMock.mockResponseOnce(JSON.stringify(errorData), { status: 400 });

    const { getByLabelText, getByText } = render(document.body.innerHTML);

    fireEvent.change(getByLabelText('Product:'), { target: { value: 1 } });
    fireEvent.change(getByLabelText('Quantity:'), { target: { value: 2 } });
    fireEvent.change(getByLabelText('Name:'), { target: { value: faker.name.fullName() } });
    fireEvent.change(getByLabelText('Email:'), { target: { value: faker.internet.email() } });
    fireEvent.change(getByLabelText('Shipping Address:'), { target: { value: faker.address.streetAddress() } });

    fireEvent.click(getByText('Place Order'));

    await waitFor(() => {
      expect(getByText('Failed to place order: Product out of stock')).toBeInTheDocument();
    });
  });

  it('should handle network error on order submission', async () => {
    fetchMock.mockRejectOnce(new Error('Network error'));

    const { getByLabelText, getByText } = render(document.body.innerHTML);

    fireEvent.change(getByLabelText('Product:'), { target: { value: 1 } });
    fireEvent.change(getByLabelText('Quantity:'), { target: { value: 2 } });
    fireEvent.change(getByLabelText('Name:'), { target: { value: faker.name.fullName() } });
    fireEvent.change(getByLabelText('Email:'), { target: { value: faker.internet.email() } });
    fireEvent.change(getByLabelText('Shipping Address:'), { target: { value: faker.address.streetAddress() } });

    fireEvent.click(getByText('Place Order'));

    await waitFor(() => {
      expect(getByText('An error occurred while placing your order.')).toBeInTheDocument();
    });
  });
});

describe('contactForm submission', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <form id="contactForm">
        <input type="text" name="name" placeholder="Name">
        <input type="email" name="email" placeholder="Email">
        <input type="text" name="subject" placeholder="Subject">
        <textarea name="message" placeholder="Message"></textarea>
        <button type="submit">Submit</button>
      </form>
    `;
  });

  it('should submit contact form', async () => {
    const contactData = {
      name: faker.name.fullName(),
      email: faker.internet.email(),
      subject: faker.lorem.sentence(),
      message: faker.lorem.paragraph(),
    };

    const consoleLogSpy = sinon.spy(console, 'log');

    const { getByLabelText, getByText } = render(document.body.innerHTML);

    fireEvent.change(getByLabelText('Name:'), { target: { value: contactData.name } });
    fireEvent.change(getByLabelText('Email:'), { target: { value: contactData.email } });
    fireEvent.change(getByLabelText('Subject:'), { target: { value: contactData.subject } });
    fireEvent.change(getByLabelText('Message:'), { target: { value: contactData.message } });

    fireEvent.click(getByText('Submit'));

    await waitFor(() => {
      expect(consoleLogSpy.calledWith('Contact form submitted:', contactData)).toBe(true);
    });

    expect(getByText('Thank you for your message! We will get back to you shortly.')).toBeInTheDocument();
  });
});