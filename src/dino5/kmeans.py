import numpy as np


class KMeans:
    """2D 데이터를 위한 K-Means 클러스터링 알고리즘"""

    def __init__(self, n_clusters=3, max_iters=100, random_state=None):
        """
        Parameters:
        -----------
        n_clusters : int
            클러스터 개수
        max_iters : int
            최대 반복 횟수
        random_state : int, optional
            난수 시드
        """
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.random_state = random_state
        self.centroids = None
        self.labels = None

    def fit(self, X):
        """
        K-Means 알고리즘 학습

        Parameters:
        -----------
        X : numpy.ndarray, shape (n_samples, 2)
            2D 입력 데이터

        Returns:
        --------
        self : KMeans
            학습된 KMeans 객체
        """
        if self.random_state is not None:
            np.random.seed(self.random_state)

        n_samples = X.shape[0]

        # 1. 초기 중심점을 랜덤하게 선택
        random_indices = np.random.choice(n_samples, self.n_clusters, replace=False)
        self.centroids = X[random_indices].copy()

        for i in range(self.max_iters):
            # 2. 각 데이터 포인트를 가장 가까운 중심점에 할당
            old_labels = self.labels
            self.labels = self._assign_clusters(X)

            # 3. 새로운 중심점 계산
            old_centroids = self.centroids.copy()
            self._update_centroids(X)

            # 4. 수렴 확인 (라벨이 변하지 않으면 종료)
            if old_labels is not None and np.array_equal(old_labels, self.labels):
                break

        return self

    def _assign_clusters(self, X):
        """
        각 데이터 포인트를 가장 가까운 중심점에 할당

        Parameters:
        -----------
        X : numpy.ndarray, shape (n_samples, 2)
            입력 데이터

        Returns:
        --------
        labels : numpy.ndarray, shape (n_samples,)
            각 데이터 포인트의 클러스터 라벨
        """
        # 각 데이터 포인트와 모든 중심점 사이의 거리 계산
        # X: (n_samples, 2), centroids: (n_clusters, 2)
        # distances: (n_samples, n_clusters)
        distances = np.sqrt(((X[:, np.newaxis] - self.centroids) ** 2).sum(axis=2))

        # 가장 가까운 중심점의 인덱스 반환
        return np.argmin(distances, axis=1)

    def _update_centroids(self, X):
        """
        각 클러스터의 새로운 중심점 계산

        Parameters:
        -----------
        X : numpy.ndarray, shape (n_samples, 2)
            입력 데이터
        """
        for k in range(self.n_clusters):
            # k번째 클러스터에 속하는 데이터 포인트들의 평균 계산
            cluster_points = X[self.labels == k]
            if len(cluster_points) > 0:
                self.centroids[k] = cluster_points.mean(axis=0)

    def predict(self, X):
        """
        새로운 데이터에 대한 클러스터 예측

        Parameters:
        -----------
        X : numpy.ndarray, shape (n_samples, 2)
            입력 데이터

        Returns:
        --------
        labels : numpy.ndarray, shape (n_samples,)
            예측된 클러스터 라벨
        """
        return self._assign_clusters(X)

    def fit_predict(self, X):
        """
        학습과 예측을 동시에 수행

        Parameters:
        -----------
        X : numpy.ndarray, shape (n_samples, 2)
            입력 데이터

        Returns:
        --------
        labels : numpy.ndarray, shape (n_samples,)
            각 데이터 포인트의 클러스터 라벨
        """
        self.fit(X)
        return self.labels


def kmeans_simple(X, n_clusters=3, max_iters=100, random_state=None):
    """
    간단한 함수형 K-Means 구현

    Parameters:
    -----------
    X : numpy.ndarray, shape (n_samples, 2)
        2D 입력 데이터
    n_clusters : int
        클러스터 개수
    max_iters : int
        최대 반복 횟수
    random_state : int, optional
        난수 시드

    Returns:
    --------
    centroids : numpy.ndarray, shape (n_clusters, 2)
        최종 중심점
    labels : numpy.ndarray, shape (n_samples,)
        각 데이터 포인트의 클러스터 라벨
    """
    if random_state is not None:
        np.random.seed(random_state)

    n_samples = X.shape[0]

    # 초기 중심점 선택
    random_indices = np.random.choice(n_samples, n_clusters, replace=False)
    centroids = X[random_indices].copy()

    for i in range(max_iters):
        # 클러스터 할당
        distances = np.sqrt(((X[:, np.newaxis] - centroids) ** 2).sum(axis=2))
        labels = np.argmin(distances, axis=1)

        # 중심점 업데이트
        old_centroids = centroids.copy()
        for k in range(n_clusters):
            cluster_points = X[labels == k]
            if len(cluster_points) > 0:
                centroids[k] = cluster_points.mean(axis=0)

        # 수렴 확인
        if np.allclose(old_centroids, centroids):
            break

    return centroids, labels


if __name__ == "__main__":
    # 테스트 코드
    # 샘플 2D 데이터 생성
    np.random.seed(42)

    # 3개의 클러스터를 가진 데이터 생성
    cluster1 = np.random.randn(50, 2) + np.array([0, 0])
    cluster2 = np.random.randn(50, 2) + np.array([5, 5])
    cluster3 = np.random.randn(50, 2) + np.array([0, 5])

    X = np.vstack([cluster1, cluster2, cluster3])

    # 클래스 기반 사용
    print("=== 클래스 기반 K-Means ===")
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X)
    print(f"중심점:\n{kmeans.centroids}")
    print(f"라벨 (처음 10개): {kmeans.labels[:10]}")

    # 함수 기반 사용
    print("\n=== 함수 기반 K-Means ===")
    centroids, labels = kmeans_simple(X, n_clusters=3, random_state=42)
    print(f"중심점:\n{centroids}")
    print(f"라벨 (처음 10개): {labels[:10]}")
