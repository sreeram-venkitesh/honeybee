# honeybee


**This honeybee collect data for the Hive Blockchain, like how real honeybees collect honey for their hives**

This is my entry for the [STEMGeek Hackathon](https://peakd.com/stem/@themarkymark/stemgeek-s-first-hackathon)

honeybee is a simple web-app that does data analytics on the blogs based on Hive. Although we have a lot of data visualization libraries in Python, it can be quite bothersome for the uninitiated and someone who just wants to get some analytics on how the various parameters vary with the different characteristics of the blogs we write. This information can be crucial in planning future blogs that can get more votes and thus get popular.

![](https://images.hive.blog/p/6VvuHGsoU2QCK6yq1XKF2z9F8sayRpwConx4qLBLTGt4gjCFNJ3P6NExZUe8GmUTvbAB9ac9o91k3xr9WDByRQVG2BwYbJKqtgo3wK3jPmgxRqisiuPRR7mgtnZyga?format=match&mode=fit)

The different features of data collection and analysis are available in the different tabs. The first tab can be used to collect the information of the latest post by searching the tag of the post. This will return information such as the name of the author, the timestamp, the total pending payout value, and so on.

![](https://images.hive.blog/p/6VvuHGsoU2QCK6yq1XKF2z9F8sayRpwConx4qLBYF7HVR5GUY9kE66PLivUjz5DE5T6BxRhn1hATuRsxnxd964DWsFwVG1emKupmhRV3BUTDhpwL5TvpQTFjcuPPU2?format=match&mode=fit)

In the Post Analytics tab, we can select what type of analysis we want to do - namely Single Characteristic Analysis and Multiple Characteristic Analysis. Single Characteristic Analysis plots the variations of a single type of data of up to the latest 100 posts of a certain tag. You can choose up to 4 different characteristics to plot at the same time. Multiple Characteristic Analysis, on the other hand, plots the relationship between the different characteristics to gain insights like how is the number of votes varying with the total number of words in the blog or how the curator rewards varying with the payout value and so on, for the last 100 posts, say.

# Future Prospects
Right now the app is just like any other product built at a hackathon. But I believe it is enough to show how promising this can become for users of Hive.

For the features that can be added to improve honeybee further.

* Complete the data analytics to include time series analysis and exploit all the capabilities of Plotly and Dash.
* Further use of Hive APIs to browse posts within the site in an easy manner, with a user-friendly UI.
* Be able to explore the blockchain blocks.
* Implement machine learning on the data collected. Regression can be done on the post details to possibly predict how new posts will perform before you post them. (I am still not quite sure if this will work perfectly, but it's still worth a try. Machine learning libraries like scikit-learn can be easily implemented within dash too.)
* The app is currently deployed on heroku, we can possibly add a custom domain.

# Links
[Live Site](hive-honey-bee.herokuapp.com)
