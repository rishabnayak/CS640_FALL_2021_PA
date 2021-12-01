# CS640 PA4 Report

## Details about the pre-processing (cleaning) step you performed

I preprocess the data to remove any tweets longer than the max tweet length, because that is bound to be garbage data. Since we're using bert-base-uncased, I convert all the tweets to lowercase, remove URL's and @mentions and replace them with spaces. I then remove nltk stopwords from the data to remove filler words and any words that don't necessarily add to the meaning of the tweet. This is followed by the removal of punctuation.

## A short description of the layers you added and your reasoning in addition to the training hyperparameters. ( Optimizer, Learning rate, batch size, Loss Function,...)

For the Naive Bayes portion of the assignment I chose to use the Complement Naive Bayes classifier since it's suited for imbalanced datasets. I tokenized the data using the RegexpTokenizer and vectorized the data using CountVectorizer.

For BERT, I chose to use the bert-base-uncased model from TFHub, along with its associated tokenizer. I chose to use a batch size of 32 because that's what the authors of BERT recommended be used for retraining the model with different data. I used the Adam optimizer with a learning rate of 2e-5, again at the author's recommendations. I chose the Binary Crossentropy Loss function because the task is essentially binary classification.

I appended a Batch Normalization layer to the pooled output from the BERT Classifier to normalize inputs for subsequent layers. This was followed by two sets of Dropout+FC Layers, and the final fully connected layer with a sigmoid activation function. The Dropout+FC layers improve the generalization performance of the model by randomly zeroing the inputs from a certain percentage of neurons making the features independent and not heavily correlated.

## The performance of your models (BERT and Bayes Classifier) on the Test-CSV provided with the dataset. For this, you can include a classification report. You are encouraged to use library functions to do this

The Bayes Classifier had a test accuracy of 82%. The precision and recall numbers were almost identical representing a well balanced dataset, and no overfitting.

The BERT Classifier had a test accuracy of 84%. Again, the precision and recall numbers were close to each other, with the precision of a zero prediction slightly higher than that of that of a one, and the recall for one was slightly higher than that of zero. However, looking at the loss and accuracy plots, overfitting is apparent - loss keeps decreasing while validation loss keeps increasing, and validation accuracy stays the same. Changing the batch size, learning rate and dropout didn't do much to change this, which leads me to believe that the amount of data I'm training with - 0.01% of the training set (due to compute time limitations) was too small for the network to converge on, and with 100M parameters, the network tried to fit the data perfectly.
