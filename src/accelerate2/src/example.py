import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from accelerate import Accelerator
from model import MNISTClassifier


def get_mnist_dataloaders(batch_size=32):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    train_dataset = datasets.MNIST(
        root='./data',
        train=True,
        download=True,
        transform=transform
    )

    test_dataset = datasets.MNIST(
        root='./data',
        train=False,
        download=True,
        transform=transform
    )

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader


def train():
    acc = Accelerator(gradient_accumulation_steps=2)

    num_epochs = 10
    learning_rate = 1e-3
    batch_size = 64

    train_loader, test_loader = get_mnist_dataloaders(batch_size)

    model = MNISTClassifier()
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.OneCycleLR(
        optimizer,
        max_lr=learning_rate,
        epochs=num_epochs,
        steps_per_epoch=len(train_loader)
    )
    criterion = nn.CrossEntropyLoss()

    model, optimizer, train_loader, test_loader, scheduler = acc.prepare(
        model, optimizer, train_loader, test_loader, scheduler
    )

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for batch_idx, (data, target) in enumerate(train_loader):
            with acc.accumulate(model):
                output = model(data)
                loss = criterion(output, target)

                acc.backward(loss)
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()

                total_loss += loss.item()

        model.eval()
        correct = 0
        total = 0

        with torch.no_grad():
            for data, target in test_loader:
                output = model(data)
                pred = output.argmax(dim=1)
                correct += (pred == target).sum().item()
                total += target.size(0)

        avg_loss = total_loss / len(train_loader)
        accuracy = 100 * correct / total

        acc.print(f"Epoch {epoch+1}/{num_epochs} - Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%")

    acc.print("Training complete!")


if __name__ == "__main__":
    train()
