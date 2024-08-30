import {boot} from "quasar/wrappers";
import PermissionsRequiredDirective from "app/directives/permissions-required-directive";

const PermissionsPlugin = {
  install(Vue: any) {
    Vue.directive('permissions-required', PermissionsRequiredDirective);
  }
};

export default boot(({app}) => {
  app.use(PermissionsPlugin);
});

