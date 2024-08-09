import {boot} from "quasar/wrappers";
import useMainStore from "stores/mainStore";
import {DirectiveBinding} from "vue";
import {Permissions} from "src/types";

export default boot(({app}) => {
  app.directive("permissions-required", {
    mounted(el, binding, vnode, old) {
      if (!useMainStore().permissions.includes(binding.value)) {
        console.log(vnode.el.parentElement)
        vnode.el.parentElement.removeChild(vnode.el)
      }
    }
  })
})
