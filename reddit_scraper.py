import praw
import pandas as pd
from datetime import datetime
import time

# Initialize Reddit API connection
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID_HERE',
    client_secret='YOUR_CLIENT_SECRET_HERE',
    user_agent='PTSDHubResearch/1.0 (by /u/YOUR_REDDIT_USERNAME)'
)

# Subreddits to monitor for PTSD community insights
subreddits = ['PTSD', 'CPTSD', 'ptsdrecovery', 'traumatoolbox']

# Data storage
all_posts = []

print("="*60)
print("PTSD Hub - Reddit Community Research Data Collection")
print("="*60)
print(f"\nStarting data collection at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Monitoring subreddits: {', '.join(subreddits)}")

# Collect data from each subreddit
for sub_name in subreddits:
    print(f"\n📊 Collecting from r/{sub_name}...")
    
    try:
        subreddit = reddit.subreddit(sub_name)
        
        # Get recent posts (last 100 new posts from each subreddit)
        for post in subreddit.new(limit=100):
            
            # Calculate post age
            post_time = datetime.fromtimestamp(post.created_utc)
            
            # Collect relevant data points
            post_data = {
                'subreddit': sub_name,
                'post_id': post.id,
                'title': post.title,
                'text': post.selftext,
                'score': post.score,
                'upvote_ratio': post.upvote_ratio,
                'num_comments': post.num_comments,
                'created_utc': post.created_utc,
                'created_date': post_time.strftime('%Y-%m-%d'),
                'created_time': post_time.strftime('%H:%M:%S'),
                'url': f"https://reddit.com{post.permalink}",
                'flair': post.link_flair_text,
                'author': str(post.author),
                'is_self': post.is_self,
                'num_crossposts': post.num_crossposts
            }
            
            all_posts.append(post_data)
        
        posts_collected = len([p for p in all_posts if p['subreddit'] == sub_name])
        print(f"   ✓ Collected {posts_collected} posts from r/{sub_name}")
        
        # Be respectful with API rate limits
        time.sleep(2)
        
    except Exception as e:
        print(f"   ✗ Error collecting from r/{sub_name}: {str(e)}")
        continue

# Convert to DataFrame for analysis
df = pd.DataFrame(all_posts)

# Generate filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'ptsd_reddit_data_{timestamp}.csv'

# Save to CSV
df.to_csv(filename, index=False, encoding='utf-8')

# Print summary statistics
print("\n" + "="*60)
print("COLLECTION COMPLETE")
print("="*60)
print(f"\n📁 Data saved to: {filename}")
print(f"📊 Total posts collected: {len(df)}")
print(f"📅 Date range: {df['created_date'].min()} to {df['created_date'].max()}")
print(f"\n📈 Posts by subreddit:")
print(df['subreddit'].value_counts().to_string())
print(f"\n💬 Average engagement:")
print(f"   - Score: {df['score'].mean():.1f}")
print(f"   - Comments: {df['num_comments'].mean():.1f}")
print(f"   - Upvote ratio: {df['upvote_ratio'].mean():.2%}")
print("\n" + "="*60)
