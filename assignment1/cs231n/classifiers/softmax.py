from random import shuffle

import numpy as np

from past.builtins import xrange


def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.

    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO:                                                                     #
    # Compute the gradient of the loss function and store it dW.                #
    # Rather that first computing the loss and then computing the derivative,   #
    # it may be simpler to compute the derivative at the same time that the     #
    # loss is being computed. You may need to modify some of the                #
    # code above to compute the gradient.                                       #
    #############################################################################

    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    num_train = X.shape[0]
    num_classes = W.shape[1]

    for t_i in xrange(num_train):
        scores_t_i = np.dot(X[t_i], W)  # Training example i x W = output
        scores_t_i -= np.max(scores_t_i)  # To avoid numerical issues
        softmax_scores = np.exp(scores_t_i) / np.sum(np.exp(scores_t_i))
        loss += -np.log(softmax_scores[y[t_i]])

        for c_i in range(num_classes):
            dW[:, c_i] += (
                (softmax_scores[c_i] - 1) * X[t_i]
                if c_i == y[t_i]
                else softmax_scores[c_i] * X[t_i]
            )

    dW /= num_train
    dW += W * reg

    loss /= num_train

    # Add regularization to the loss.
    loss += 0.5 * reg * np.sum(W ** 2)
    #############################################################################
    #                          END OF YOUR CODE                                 #
    #############################################################################

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    num_train = X.shape[0]
    scores = np.dot(X, W)
    scores -= np.max(scores, axis=1, keepdims=True)  # Numerical stability
    softmax_scores = np.exp(scores)/np.sum(np.exp(scores), axis=1, keepdims=True)
    loss = np.sum(-np.log(softmax_scores[np.arange(num_train), y])) / num_train

    # Add regularization to the loss.
    loss += 0.5 * reg * np.sum(W ** 2)

    scores_derivative = softmax_scores
    scores_derivative[np.arange(num_train), y] -= 1

    dW = np.dot(X.T, scores_derivative) / num_train
    dW += W * reg
    #############################################################################
    #                          END OF YOUR CODE                                 #
    #############################################################################

    return loss, dW
