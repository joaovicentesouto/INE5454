// Listagem dos aplicativos que possuem uma ou mais categorias específicas.
db.AppsCollection.find(
	{
		"categories" : {$eq : "art", $eq : "design"}
	}
)

// // Listagem, com uma dada ordenação, dos aplicativos que possuem determinadas categorias e avaliação acima de um dado valor.
// db.AppsCollection.find(
// 	{
// 		"categories" : {$eq : "games"},
// 		"rating" : {$gt:3}
// 	}
// ).sort(
// 	{
// 		"rating" : -1
// 	}
// )

// // Quantidade de aplicativos de uma determinada categoria por loja (Google, Apple ou Shopify).
// db.AppsCollection.find(
// 	{
// 		"categories" : {$eq : "games"},
// 		"shopify_apps" : {$exists : true}
// 	}
// ).count()

// db.AppsCollection.find(
// 	{
// 		"categories" : {$eq : "games"},
// 		$or : [
// 			{"apple_apps" : {$exists : true}},
// 			{"google_apps" : {$exists : true}}
// 		]
// 	}
// ).count()

// // Listagem das categorias que frequentemente estão associadas à uma categoria específica.
// db.AppsCollection.find(
// 	{
// 		"categories" : {$eq : "games"}
// 	}
// )

db.AppsCollection.aggregate([
    {
		'$match' : {'categories': {$eq : "games"}}
	},
	{
		$group: {
			_id: null, 
			count: {
			  $sum: 1
			}
		  }
	}
])

// // Preço mínimo, máximo, médio e mediano dos aplicativos de uma determinada categoria por loja.
// db.AppsCollection.find(
// 	{
// 		"categories" : {$eq : "games"},
// 		$or : [
// 			{"apple_apps" : {$exists : true}},
// 			{"google_apps" : {$exists : true}},
// 			{"shopify_apps" : {$exists : true}}
// 		]
// 	}
// )
