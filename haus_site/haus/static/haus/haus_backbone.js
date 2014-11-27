/* Sets up the models, views, and router for the main HAUS site */

var Device = Backbone.Model.extend({
  urlRoot: '/devices',
});

var DeviceList = Backbone.Collection.extend({
  model: Device,
  url: '/devices',
});

var DeviceListView = Backbone.View.extend({

  initialize:function () {
    this.model.bind("reset", this.render, this);
    this.listenTo(this.model, 'change', this.render);
  },

  render:function () {
    $(this.el).empty();
    _.each(this.model.models, function (device) {
      $(this.el).append(new DeviceView({model:device}).render().el);
    }, this);
    return this;
  },
});

var DeviceView = Backbone.View.extend({
  tagName:'div',
  className:'sidebar-item',

  events: {
    'click span': 'displayatoms',
  },

  render:function (eventName) {
    var model_info = "Pk: " + this.model.get('pk') +
                     "\nName: <span>" + this.model.get('name') + "</span>" +
                     "\nAtoms: " + String(this.model.get('atoms'));
    $(this.el).html(model_info);
    return this;
  },

  displayatoms: function (event) {
    atomsView = new AtomsView({model: this.model});
    atomsView.render();
  },
});

var AtomsView = Backbone.View.extend({
  tagName: 'div',
  className: 'monitor',

  render:function () {
    console.log(this.model);
    container_div = $('.main-box').empty();
    $(this.el).append('<div class="title-box">' + this.model.get('name') + "</div>")
    _.each(this.model.get('atoms'), function (atom) {
      $(this.el).append('<p>' + atom + '</p>');
    }, this);
    container_div.append($(this.el));
    return this;
  },
});

// ROUTER GOES HERE
var AppRouter = Backbone.Router.extend({
  routes: {
    "devices/:id": "showDeviceAtoms",
    "*actions": "defaultRoute", // matches http://example.com/#anything-here
  }
});

var app_router = new AppRouter();

app_router.on('route:defaultRoute', function () {
  this.devices = new DeviceList();
  this.devicesView = new DeviceListView({model: this.devices, el: $('.sidebar')});

  this.devices.fetch({success: function (model) {
    model.trigger('change');
  }});
});

app_router.on('route:showDeviceAtoms', function (id) {
  this.trigger('route:defaultRoute');
});
// Start Backbone history a necessary step for bookmarkable URL's
Backbone.history.start();


