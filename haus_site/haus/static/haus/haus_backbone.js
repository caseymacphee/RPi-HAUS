/* Sets up the models, views, and router for the main HAUS site */

var Device = Backbone.Model.extend({
  urlRoot: '/devices',
});

var DeviceList = Backbone.Collection.extend({
  model: Device,
  url: '/devices',
});

var Atom = Backbone.Model.extend({
  url: function () {
    //This probably doesn't work, but you get the idea
    //return '/devices/' + this.device.id + '/atom/' + this.id + '/current';
    return '/devices/1/atom/1/current';  //Testing testing testing
  },
});

var DeviceCurrent = Backbone.Collection.extend({
  model: Atom,
  url: function () {
    return '/devices/' + this.id + '/current/';
  },
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
    'click a': 'display_current_values',
  },

  render:function (eventName) {
    var model_info = "<a href='#'>" + this.model.get('device_name')+ "</a>";
    $(this.el).html(model_info);
    return this;
  },

  display_current_values: function (event) {
    id = this.model.get('id');
    name = this.model.get('device_name');
    current_device = new DeviceCurrent();
    current_device.id = id;
    current_device.device_name = name;
    current_device.fetch({success: function (model) {
        atomsView = new AtomsView({model: model});
        atomsView.render();
      }
    });
  },
});

var AtomsView = Backbone.View.extend({
  tagName: 'div',
  className: 'monitor',

  render:function () {
    container_div = $('.main-box').empty();
    $(this.el).append('<div class="title-box">' + this.model.device_name + "</div>");
    this.atoms = this.model.models;
    _.each(this.model.models, function (atom) {
      if (atom.has('atom_name')) {
        $(this.el).append('<p>' + atom.get('atom_name') + ': ' + atom.get('value') + '</p>');
      }
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
  this.devicesView = new DeviceListView({model: this.devices, el: $('#device_links')});

  this.devices.fetch({success: function (model) {
    model.trigger('change');
  }});
});

app_router.on('route:showDeviceAtoms', function (id) {
  this.trigger('route:defaultRoute');
});
// Start Backbone history a necessary step for bookmarkable URL's
Backbone.history.start();


