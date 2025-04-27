import {boot} from "quasar/wrappers";
import PermissionsRequiredDirective from "app/directives/permissions-required-directive";
import dayjs from "dayjs";
import 'dayjs/locale/ru';

const PermissionsPlugin = {
  install(Vue: any) {
    Vue.directive('permissions-required', PermissionsRequiredDirective);
    dayjs.locale('ru') // use locale globally

  }
};

export default boot(({app}) => {
  app.use(PermissionsPlugin);
});

