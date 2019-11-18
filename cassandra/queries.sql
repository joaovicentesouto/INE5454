Listagem dos reviews de um ou mais aplicativo

SELECT * FROM test.reviews WHERE app_id = 123 ALLOW FILTERING; -- [OR app_id = 101010101, ...]

Listagem dos comentários com rating baixo (ou alto) de um ou mais aplicativos

SELECT *
FROM test.reviews
WHERE app_id = 123
ORDER BY rating ASC; -- DESC

Listagem dos comentários com sentimento mais negativo (ou positivo) de um ou mais aplicativos

SELECT *
FROM test.reviews
WHERE app_id = 123
ORDER BY sentiment_polarity DESC; -- ASC
