# review
I only created one store in facebook: https://www.facebook.com/people/Store-1/100091278542317/?sk=reviews, the pageID is: 117623211277081

Get review http://localhost:5005/review/"int:pageID" [GET]. Dont need any json input. 

Sample output:
{
    "data": [
        {
            "created_time": "2023-03-26T20:42:47+0000",
            "recommendation_type": "negative",
            "review_text": "There are lots of stalls close down due to the current economic. I sincerely hope this stall is one of them."
        },
        {
            "created_time": "2023-03-26T20:30:15+0000",
            "recommendation_type": "positive",
            "review_text": "Dame nice, can taste the freshness"
        }
    ]
}
