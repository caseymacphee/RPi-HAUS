/* Sets up the models, views, and router for the main HAUS site */

var Device = Backbone.Model.extend({
  urlRoot: '/devices',
});

var DeviceList = Backbone.Collection.extend({
  model: Device,
  url: '/devices',
});

var AtomCurrent = Backbone.Model.extend({
  url: function () {
    //This probably doesn't work, but you get the idea
    //We don't fetch this directly anyway
    //return '/devices/' + this.device.id + '/atom/' + this.id + '/current';
    return '/devices/1/atom/1/current';  //Testing testing testing
  },
});

var DeviceCurrent = Backbone.Collection.extend({
  model: AtomCurrent,

  url: function () {
    return '/devices/' + this.id + '/current/';
  },

  startPolling : function(interval){
    this.Polling = true;
    if( interval ){
      this.interval = interval;
    }
    this.executePolling(this, null, null);
  },

  stopPolling : function(){
    this.Polling = false;
  },

  executePolling : function(model, response, options){
    this.fetch({success : model.onFetch});
  },

  onFetch : function (model, response, options) {
    if( model.Polling ){
      setTimeout(function () {
        model.executePolling(model, null, null);
      }, model.interval);
    }
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

  initialize:function () {
    this.model.bind("reset", this.render, this);
    this.listenTo(this.model, 'draw', this.click_handler);
  },

  events: {
    'click': 'click_handler',
  },

  click_handler: function () {
    if (typeof current_device !== 'undefined') {
      current_device.stopPolling();
    }
    current_device = new DeviceCurrent();
    current_device.id = this.model.get('id');
    current_device.device_name = this.model.get('device_name');
    current_device.fetch({success: function (model) {
      atomsView = new AtomsView({model: model});
      atomsView.render();
      model.startPolling(15000); //Every 15 seconds
      app_router.navigate('/devices/' + model.id);
    }});
  },

  render: function (eventName) {
    var model_info = this.model.get('device_name');
    $(this.el).text(model_info);
    return this;
  },

});

var AtomsView = Backbone.View.extend({
  tagName: 'div',
  className: 'monitor',

  initialize:function () {
    this.model.bind("reset", this.render, this);
    this.listenTo(this.model, 'change', this.render);
  },

  render:function () {
    container_div = $('.main-box').empty();
    $(this.el).append('<div class="title-box">' + this.model.device_name + "</div>");
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
  this.devices = new DeviceList();
  this.devicesView = new DeviceListView({model: this.devices, el: $('#device_links')});
  this.devices.fetch({success: function (model) {
    model.trigger('change');
    device = model.get(id);
    device.trigger('draw');
  }});
});

// Start Backbone history a necessary step for bookmarkable URL's
Backbone.history.start();


