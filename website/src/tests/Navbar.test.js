import { render, screen } from '@testing-library/react';
import Navbar from '../components/Navbar';

test('Renders the Navbar', () => {
  render(<Navbar />);
  const Element = screen.getByText(/House Plants Manager/i);
  expect(Element).toBeInTheDocument();
});
