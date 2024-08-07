a
    X͞f  �                   @   s~  d dl Z d dlZd dlZd dlm  mZ d dlmZ dd� Z	dZ
e	e
�Zedurhed� ee�� � ned� dgZg ZeD ]>\Z
Ze	e
�e ZZedur�e�eef� q~ed	e� d
�� q~dZeD ]X\ZZede� d�7 Zej�sejddd�Zede� d�7 Zee7 Zq�ede� d�7 Zq�ed7 Zed� eedd� � edddd��Ze�e� W d  � n1 �sp0    Y  dS )�    N)�datetimec              
   C   s,  t d| � �� z�ddd�}tj| |d�}|jdkr�t�|j�}g }|�d�D ]�}|�d�j	}|�d	�j	}|�d
�j	}|�d�j	}	t d|� �� t d|� �� t d|� �� t d|	� d�� |�
||||	d�� qLt�|�}
|
W S t d|j� �� W n4 t�y& } zt d|� �� W Y d }~n
d }~0 0 d S )NzFetching news from: zsMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36zapplication/xml)z
User-AgentZAccept)�headers��   z.//item�title�linkZpubDateZdescriptionzTitle: zLink: zPublished Date: z	Summary: �
)ZTitleZLinkzPublished DateZSummaryz'Failed to fetch RSS feed, status code: zFailed to fetch RSS feed: )�print�requests�getZstatus_code�ETZ
fromstringZcontent�findall�find�text�append�pdZ	DataFrame�	Exception)�urlr   Zresponse�rootZ	news_list�itemr   r   Zpublished_dateZsummary�df�e� r   �Mc:\Users\Lenovo\Documents\GitHub\news\.github\workflows\scripts\fetch_news.py�get_news_from_rss   s<    �
�

$r   �Ohttps://www.reutersagency.com/feed/?best-topics=business-finance&post_type=bestz
DataFrame:z*No se pudieron obtener datos del RSS feed.)r   ZReuterszFailed to fetch data for �.z0<html><head><title>RSS News</title></head><body>z<h2>z</h2>F)�index�escapez<h3>Data for z</h3>z<p>No data available for z</p>z</body></html>zHTML Content Preview:i�  zdocs/index.html�wzutf-8)�encoding)Z
feedparserZpandasr   r	   Zxml.etree.ElementTreeZetreeZElementTreer   r   r   r   Znews_dfr   �headZ	rss_feedsZall_newsZsource_name�sourcer   Zhtml_content�emptyZto_htmlZdf_html�open�f�writer   r   r   r   �<module>   s@   4�
