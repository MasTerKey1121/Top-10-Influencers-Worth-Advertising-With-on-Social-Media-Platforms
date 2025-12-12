# 📢 Top 10 Influencers Worth Advertising With (Social Media Analytics)

A data analytics pipeline designed to identify high-potential influencers for marketing campaigns. This project integrates static datasets with real-time API data to calculate engagement rates and segment influencers based on their audience size.

![Python](https://img.shields.io/badge/Python-3.9-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-Data%20Lake-green)
![MySQL](https://img.shields.io/badge/MySQL-Structured%20DB-orange)
![YouTube API](https://img.shields.io/badge/YouTube%20Data%20API-v3-red)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c)

## 🏗️ System Architecture & Logic

The project follows a **Hybrid Database Architecture**, utilizing MongoDB as a Data Lake for raw data and MySQL for structured, enriched data.

```mermaid
graph TD
    A[Kaggle Dataset] -->|Ingest Raw Data| B(MongoDB Data Lake)
    B -->|Extract Channel Names| C{YouTube Data API v3}
    C -->|Fetch Real-time Stats| D[MySQL Database]
    D -->|Calculate Engagement| E[Data Transformation]
    E -->|Segment by Followers| F[Influencer Types]
    F -->|Visualize| G[Matplotlib Dashboard]

```
Canva presentation  : https://www.canva.com/design/DAGhmc_MCBc/DGPy8PQXSVmoqZ4bzs5ggA/edit?utm_content=DAGhmc_MCBc&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton  

Kaggle Data set : https://www.kaggle.com/datasets/ramjasmaurya/top-1000-social-media-channels
