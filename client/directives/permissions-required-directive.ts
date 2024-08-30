import useMainStore from "stores/mainStore";

export default {
  mounted(el: any, binding: any, vnode: any) {
    if (!useMainStore().permissions.includes(binding.value)) {
      vnode.el.parentElement.removeChild(vnode.el)
    }
  },
};
