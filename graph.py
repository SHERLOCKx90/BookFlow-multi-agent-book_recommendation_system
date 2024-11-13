import matplotlib.pyplot as plt

# Example MRR values for different recommendation models
iterations = range(1, 6)  # Five sample iterations for demonstration
mrr_collaborative = [0.15, 0.18, 0.22, 0.24, 0.26]
mrr_content_based = [0.16, 0.20, 0.23, 0.27, 0.29]
mrr_sentiment_based = [0.17, 0.19, 0.22, 0.25, 0.27]
mrr_hybrid = [0.18, 0.22, 0.26, 0.30, 0.34]

# Plotting the MRR comparison as a line chart
plt.figure(figsize=(10, 6))

plt.plot(iterations, mrr_collaborative, marker='o', label='Collaborative Filtering', linestyle='--')
plt.plot(iterations, mrr_content_based, marker='s', label='Content-Based Filtering', linestyle='--')
plt.plot(iterations, mrr_sentiment_based, marker='^', label='Sentiment-Based Filtering', linestyle='--')
plt.plot(iterations, mrr_hybrid, marker='D', label='Hybrid Model', color='black', linewidth=2)

# Adding titles and labels
plt.title('Mean Reciprocal Rank (MRR) Comparison Across Models')
plt.xlabel('Iterations')
plt.ylabel('Mean Reciprocal Rank (MRR)')
plt.legend(loc='lower right')
plt.grid(True)

# Display the chart
plt.show()
