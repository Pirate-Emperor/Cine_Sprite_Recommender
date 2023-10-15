import numpy as np
import pandas as pd 
ratings_df = pd.read_csv('small_movie_ratings1.csv', index_col=0)
print(ratings_df)


def find_correlation_between_two_users(ratings_df: pd.DataFrame, user1: str, user2: str):
    """Find correlation between two users based on their rated movies using Pearson correlation"""
    rated_movies_by_both = ratings_df[[user1, user2]].dropna(axis=0).values
    user1_ratings = rated_movies_by_both[:, 0]
    user2_ratings = rated_movies_by_both[:, 1]
    return np.corrcoef(user1_ratings, user2_ratings)[0, 1]
users = list(ratings_df.columns)
movies = list(ratings_df.index)
similarity_matrix = np.array([[find_correlation_between_two_users(ratings_df, user1, user2) for user1 in users] for user2 in users])
similarity_df = pd.DataFrame(similarity_matrix, columns=users, index=users)
print(similarity_df)


def get_rated_user_for_a_movie(ratings_df: pd.DataFrame, movie: str):
    return ratings_df.loc[movie, :].dropna().index.values

def get_top_neighbors(similarity_df: pd.DataFrame, user: str, rated_users: str, n_neighbors: int):
    return similarity_df[user][rated_users].nlargest(n_neighbors).to_dict()

def subtract_bias(rating: float, mean_rating: float):
    return (rating - mean_rating) if (rating - mean_rating>0) else 0.1


def get_neighbor_rating_without_bias_per_movie(
    ratings_df: pd.DataFrame, user: str, movie: str
):
    """Substract the rating of a user from the mean rating of that user to eliminate bias"""
    mean_rating = ratings_df[user].mean()
    rating = ratings_df.loc[movie, user]
    return subtract_bias(rating, mean_rating)
    
def get_ratings_of_neighbors(ratings_df: pd.DataFrame, neighbors: list, movie: str):
    """Get the ratings of all neighbors after adjusting for biases"""
    return [
        get_neighbor_rating_without_bias_per_movie(ratings_df, neighbor, movie)
        for neighbor in neighbors
    ]

def get_weighted_average_rating_of_neighbors(ratings: list, neighbor_distance: list):
    weighted_sum = np.array(ratings).dot(np.array(neighbor_distance))
    abs_neigbor_distance = np.abs(neighbor_distance)
    return weighted_sum / np.sum(abs_neigbor_distance)

def ger_user_rating(ratings_df: pd.DataFrame, user: str, avg_neighbor_rating: float):
    user_avg_rating = ratings_df[user].mean()
    return round(user_avg_rating + avg_neighbor_rating, 2)

def predict_rating(
    df: pd.DataFrame,
    similarity_df: pd.DataFrame,
    user: str,
    movie: str,
    n_neighbors: int = 2,
):
    """Predict the rating of a user for a movie based on the ratings of neighbors"""
    ratings_df = df.copy()

    rated_users = get_rated_user_for_a_movie(ratings_df, movie)

    top_neighbors_distance = get_top_neighbors(
        similarity_df, user, rated_users, n_neighbors
    )
    neighbors, distance = top_neighbors_distance.keys(), top_neighbors_distance.values()

    print(f"Top {n_neighbors} neighbors of user {user}, {movie}: {list(neighbors)}")

    ratings = get_ratings_of_neighbors(ratings_df, neighbors, movie)
    avg_neighbor_rating = get_weighted_average_rating_of_neighbors(
        ratings, list(distance)
    )

    return ger_user_rating(ratings_df, user, avg_neighbor_rating)

full_ratings = ratings_df.copy()

for user, movies in full_ratings.iteritems():
    for movie in movies.keys():
        if np.isnan(full_ratings.loc[movie, user]):
            full_ratings.loc[movie, user] = predict_rating(
                ratings_df, similarity_df, user, movie
            )
print(full_ratings)
full_ratings.to_csv("full_ratings1.csv")