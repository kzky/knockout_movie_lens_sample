ko.observableArray.fn.pushAll = function(valuesToPush) {
    var underlyingArray = this();
    this.valueWillMutate();
    ko.utils.arrayPushAll(underlyingArray, valuesToPush);
    this.valueHasMutated();
    return this;
}

// Not to be used here.
function User(user_name) {
    var self = this
    self.user_name = user_name
}

function Movie(movie_name) {
    var self = this
    self.movie_name = movie_name
}

function C2CResult(movie, score) {
    var self = this
    self.movie = movie
    self.score = score
}

// ViewModel
function RecommendationViewModel() {
    var self = this

    self.users = ko.observableArray()
    self.movies = ko.observableArray()
    self.c2cResults = ko.observableArray()

    self.getUsers = function() {
        self.c2cResults.removeAll()
        self.movies.removeAll()
        
        url = "http://localhost:8080/api/movie_lens/users"
        data = {"limit": 30}
        $.get(url, data, function (data) {
            users = JSON.parse(data)
            console.log(users);
            self.users.pushAll(users);
        })
    }

    self.getMovies = function(user_name) {
        self.c2cResults.removeAll()
        self.movies.removeAll()
        
        url = "http://localhost:8080/api/movie_lens/users/" + user_name
        data = {"limit": 30}
        $.get(url, data, function(data) {
            movies = JSON.parse(data)
            console.log(movies);
            self.movies.pushAll(movies)
        })
    }

    self.getC2CResults = function(movie_name) {
        self.c2cResults.removeAll()
        
        url = "http://localhost:8080/api/movie_lens/c2c_results/" + movie_name
        data = {"limit": 30}
        $.get(url, data, function(data) {
            c2cResults = JSON.parse(data)
            self.c2cResults.pushAll(c2cResults)
        })
    }
}

recommendationVm =  new RecommendationViewModel()
recommendationVm.users.removeAll()
recommendationVm.getUsers()
ko.applyBindings(recommendationVm)
