import unittest
import torch
from models.color_model import ColorModel


class ColorModelTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.input_dim = 3
        self.output_dim = 1
        self.model = ColorModel(input_dim=self.input_dim, output_dim=self.output_dim)

    def test_model_initialization(self):
        """Test that model initializes with correct architecture"""
        self.assertIsInstance(self.model, ColorModel)
        self.assertIsInstance(self.model.network, torch.nn.Sequential)

    def test_forward_pass(self):
        """Test forward pass produces output of correct shape"""
        input_tensor = torch.FloatTensor([[0.5, 0.8, 0.6]])
        output = self.model(input_tensor)
        self.assertEqual(output.shape, (1, self.output_dim))

    def test_output_range(self):
        """Test that output is in valid range [0, 1] due to Sigmoid"""
        input_tensor = torch.FloatTensor([[0.5, 0.8, 0.6]])
        output = self.model(input_tensor)
        self.assertTrue(torch.all(output >= 0))
        self.assertTrue(torch.all(output <= 1))

    def test_batch_processing(self):
        """Test model can process batches of inputs"""
        batch_size = 5
        input_tensor = torch.rand(batch_size, self.input_dim)
        output = self.model(input_tensor)
        self.assertEqual(output.shape, (batch_size, self.output_dim))

    def test_different_input_values(self):
        """Test model with different input values"""
        inputs = [
            torch.FloatTensor([[0.0, 0.0, 0.0]]),
            torch.FloatTensor([[1.0, 1.0, 1.0]]),
            torch.FloatTensor([[0.5, 0.5, 0.5]]),
        ]
        for input_tensor in inputs:
            output = self.model(input_tensor)
            self.assertEqual(output.shape, (1, self.output_dim))
            self.assertTrue(torch.all(output >= 0))
            self.assertTrue(torch.all(output <= 1))

    def test_gradient_flow(self):
        """Test that gradients flow through the network"""
        input_tensor = torch.FloatTensor([[0.5, 0.8, 0.6]])
        input_tensor.requires_grad = True
        output = self.model(input_tensor)
        loss = output.sum()
        loss.backward()
        self.assertIsNotNone(input_tensor.grad)

    def test_eval_mode(self):
        """Test switching to evaluation mode"""
        self.model.eval()
        self.assertFalse(self.model.training)

    def test_train_mode(self):
        """Test switching to training mode"""
        self.model.train()
        self.assertTrue(self.model.training)


if __name__ == '__main__':
    unittest.main()
