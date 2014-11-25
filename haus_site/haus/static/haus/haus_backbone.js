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

  render:function (eventName) {
    var model_info = "Pk: " + this.model.get('pk') +
                     "\nName: " + this.model.get('name') +
                     "\nAtoms: " + String(this.model.get('atoms'));
    $(this.el).text(model_info);
    return this;
  }
});

// ROUTER GOES HERE
var devices = new DeviceList();
var devicesView = new DeviceListView({model: this.devices, el: $('.sidebar')});

devices.fetch({success: function () {
  devicesView.render();
}});
