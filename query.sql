-- include the number of posts each user has created
SELECT users.id AS user_id, email, COUNT(posts.owner_id) as num_of_posts
FROM users
LEFT JOIN posts ON posts.owner_id = users.id -- outer join by default
GROUP BY users.id;

-- with right join, just for sql practice
-- SELECT users.id AS user_id, users.email AS user_email, COUNT(posts.id) AS num_of_posts
-- FROM posts 
-- RIGHT JOIN users ON posts.owner_id = users.id
-- GROUP BY users.id;

-- include the number of votes each post has
SELECT posts.* , COUNT(votes.post_id) as votes 
FROM posts
LEFT JOIN votes ON posts.id = votes.post_id
GROUP BY posts.id;