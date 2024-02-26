import numpy as np
from sklearn.datasets import make_classification, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sympy import symbols, Eq, nsolve, sqrt, log, exp

RANDOM_STATE = 1


def get_param(epsilon, delta, epochs):
    delta_u = delta / (epochs + 1)
    x = symbols('x')
    equation = Eq(sqrt(2 * epochs * log(1 / delta_u)) *
                  x + epochs * x * (exp(x) - 1), epsilon)
    epsilon_u = nsolve(equation, x, epsilon / epochs)
    return epsilon_u, delta_u


class LogisticRegressionCustom:
    def __init__(self, learning_rate=0.01, num_iterations=100):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.tau = 1e-6  # small value to prevent log(0)
        self.weights = None
        self.bias = None

    def sigmoid(self, z):
        # np.clip(z, -500, 500) limits the range of z to avoid extremely
        # large or small values that could lead to overflow.
        return 1 / (1 + np.exp(-np.clip(z, -700, 700)))

    def fit(self, X, y):
        # Initialize weights and bias
        num_samples, num_features = X.shape
        self.weights = np.zeros(num_features)
        self.bias = 0.0

        # Gradient descent optimization
        for _ in range(self.num_iterations):
            # Compute predictions of the model
            linear_model = np.dot(X, self.weights) + self.bias
            predictions = self.sigmoid(linear_model)

            # Compute loss and gradients
            loss = -np.mean(
                y * np.log(predictions + self.tau)
                + (1 - y) * np.log(1 - predictions + self.tau)
            )
            dz = predictions - y
            dw = np.dot(X.T, dz) / num_samples
            db = np.sum(dz) / num_samples

            # Update weights and bias
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def dp_fit(self, X, y, epsilon, delta, C=1):
        # Initialize weights and bias
        num_samples, num_features = X.shape
        self.weights = np.zeros(num_features)
        self.bias = 0

        # Gradient descent optimization
        for _ in range(self.num_iterations):
            # Compute predictions of the model
            linear_model = np.dot(X, self.weights) + self.bias
            predictions = self.sigmoid(linear_model)

            # Compute loss and gradients
            loss = -np.mean(y * np.log(predictions + self.tau) + (1 - y)
                            * np.log(1 - predictions + self.tau))
            dz = predictions - y

            # TODO: Clip gradient here.
            clip_dz = clip_gradients(dz, C)
            # Add noise to gradients
            # TODO: Calculate epsilon_u, delta_u based epsilon, delta and epochs here.
            """
               经过 num_iterations 次迭代后需要达到 epsilon, delta 的差分隐私，那么每次迭代的隐私预算为 epsilon_u, delta_u = epsilon / num_iterations, delta / num_iterations
            """
            # epsilon_u, delta_u = epsilon / self.num_iterations, delta / self.num_iterations
            epsilon_u, delta_u = get_param(epsilon, delta, self.num_iterations)
            noisy_dz = add_gaussian_noise_to_gradients(
                clip_dz, epsilon_u, delta_u, C)

            dw = np.dot(X.T, noisy_dz) / num_samples
            db = np.sum(noisy_dz) / num_samples

            # Update weights and bias
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict_probability(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        probabilities = self.sigmoid(linear_model)
        return probabilities

    def predict(self, X):
        probabilities = self.predict_probability(X)
        # Convert probabilities to classes
        return np.round(probabilities)


def get_train_data(dataset_name=None):
    if dataset_name is None:
        # Generate simulated data
        # np.random.seed(RANDOM_STATE)
        X, y = make_classification(
            n_samples=1000, n_features=20, n_classes=2, random_state=RANDOM_STATE
        )
    elif dataset_name == "cancer":
        # Load the breast cancer dataset
        data = load_breast_cancer()
        X, y = data.data, data.target
    else:
        raise ValueError("Not supported dataset_name.")

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    return X_train, X_test, y_train, y_test


def clip_gradients(gradients, C):
    """
    max 保存的是梯度的最大值，如果梯度的最大值大于C，那么就将梯度除以最大值，使得梯度的最大值等于C
        用于梯度裁剪，而梯度裁剪的目的是为了防止梯度爆炸，梯度爆炸会导致模型的参数更新过大，从而导致模型的不稳定
    由于 numpy 具有广播的特性，所以直接将 gradients 除以 max 即可
    """
    max = np.maximum(1, np.linalg.norm(gradients, ord=2) / C)
    clip_gradients = gradients / max
    return clip_gradients


def add_gaussian_noise_to_gradients(gradients, epsilon, delta, C):
    """
    sigma 用于求高斯分布的标准差，sigma = (b - a) / (2 * delta) * sqrt(2 * log(1.25 / delta))
    noise 用于生成高斯噪声，np.random.normal 即用于生成高斯噪声
    """
    sigma = np.ptp(gradients) * np.sqrt(2 * np.log(1.25 / delta)) / epsilon
    noise = np.random.normal(loc=0, scale=sigma * C, size=gradients.shape)
    noisy_gradients = noise + gradients
    return noisy_gradients


if __name__ == "__main__":
    # Prepare datasets.
    dataset_name = "cancer"
    X_train, X_test, y_train, y_test = get_train_data(None)

    # Training the normal model
    normal_model = LogisticRegressionCustom(
        learning_rate=0.01, num_iterations=1000)
    normal_model.fit(X_train, y_train)
    y_pred = normal_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Normal accuracy:", accuracy)

    # Training the differentially private model
    dp_model = LogisticRegressionCustom(
        learning_rate=0.01, num_iterations=1000)
    epsilon, delta = 0.1, 1e-3
    dp_model.dp_fit(X_train, y_train, epsilon=epsilon, delta=delta, C=1)
    y_pred = dp_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("DP accuracy:", accuracy)
