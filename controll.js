var fs = require('fs');
var mongoose = require('mongoose');
/////test

module.exports = function(app,db)
{
	app.get('/food', function(req,res){
		user_id = req.query.fid;
    title = req.query.title;
		var collection = db.collection('foods');
    var collection_storage = db.collection('storage');
    if(title){
      collection.find({title: {$regex : ".*"+title+".*"}}).sort({"rank":1}).toArray(function (err, result) {
        if (err) {
          console.log(err);
        } else {
          var json = '{\"results\":' + JSON.stringify(result,null,4) + '}';
          res.header("Content-Type", "application/json; charset=utf-8");
          res.write(json);
          res.end();
        }
      });
    }else if(user_id){
      collection_storage.findOne({'fid':user_id},function(err, result){
        var ingredients = result.ingredients;
        console.log(ingredients);
        collection.find().sort({"rank":1}).toArray(function (err, result2) {
          var result_exact = [];
          for(var i =0;i<result2.length;i++){
            var dup_list = result2[i].main_ingredients.filter(function(val) {
              return ingredients.indexOf(val[0]) != -1;

            });
            if(dup_list.length>0)
              console.log(dup_list.length);
            if(dup_list.length/result2[i].main_ingredients.length>0.5){
              result_exact.push(result2[i]);
            }
          }
          if (err) {
            console.log(err);
          } else {
            var json = '{\"results\":' + JSON.stringify(result_exact,null,4) + '}';
            res.header("Content-Type", "application/json; charset=utf-8");
            res.write(json);
            res.end();
          }
        });
      });
    }


	});
  app.get('/ingredients', function(req,res){
		var collection = db.collection('ingredients');
    collection.find().toArray(function (err, result) {
      if (err) {
        console.log(err);
      } else {
        var json = '{\"results\":' + JSON.stringify(result,null,4) + '}';
        res.header("Content-Type", "application/json; charset=utf-8");
        res.write(json);
        res.end();
      }
    });
});
    app.get('/storage', function(req,res){
      user_id = req.query.fid;
  		var collection = db.collection('storage');
      collection.find({'fid':user_id}).toArray(function (err, result) {
        if (err) {
          console.log(err);
        } else {
          var json = '{\"results\":' + JSON.stringify(result,null,4) + '}';
          res.header("Content-Type", "application/json; charset=utf-8");
          res.write(json);
          res.end();
        }
      });
});
  app.post('/storage', function (req, res) {
    console.log(JSON.stringify(req.body,null,4));
    user_id = req.body.fid;
    ingredient = req.body.ingredient;
    var collection = db.collection('storage');
    collection.update(
      {'fid':user_id},
      {$addToSet: {'ingredients':ingredient}},
      {upsert: true,setDefaultsOnInsert: true},
      function (err, result) {
        if (err) {
          console.log(err);
        } else {
          console.log(result.n);
          res.header("Content-Type", "application/json; charset=utf-8");
          var json = '{\"results\":' + JSON.stringify(result,null,4) + '}';
          res.write(json);
          res.end();
        }
      }
    );
});

app.delete('/storage', function (req, res) {
  user_id = req.body.fid;
  ingredient = req.body.ingredient;
  var collection = db.collection('storage');
  collection.update(
    {'fid':user_id},
    {$pull: {'ingredients':ingredient}},
    {upsert: true,setDefaultsOnInsert: true},
    function (err, result) {
      if (err) {
        console.log(err);
      } else {
        console.log(result.n);
        res.header("Content-Type", "application/json; charset=utf-8");
        var json = '{\"results\":' + JSON.stringify(result,null,4) + '}';
        res.write(json);
        res.end();
      }
    }
  );
});


};
