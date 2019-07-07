# https://gist.github.com/entaroadun/1653794

import numpy as np
from lightfm.datasets import fetch_movielens
from lightfm import LightFM

# Fetch data and format it
data = fetch_movielens(min_rating=4.0)

print("hello world!")
print(repr(data['train']))
print(repr(data['test']))


# create model
model = LightFM(loss='warp')
# train model
model.fit(data['train'], epochs=30, num_threads=2)


def sample_recommendation(model, data, user_ids):
    n_users, n_items = data['train'].shape

    # generate recommendation
    for user_id in user_ids:
        # movies they already like
        known_positives = data['item_labels'][data['train']
                                              .tocsr()[user_id].indices]

        # movies our model predicts
        scores = model.predict(user_id, np.arange(n_items))

        # rank in order of most liked to least
        top_items = data['item_labels'][np.argsort(~scores.astype(np.int))]

        print("User %s" % user_id)
        print("Known positives: ")

        for x in known_positives[: 3]:
            print("            %s" % x)

        print("      Recommended:")
        for x in top_items[: 3]:
            print("            %s" % x)


sample_recommendation(model, data, [3, 25, 450])
