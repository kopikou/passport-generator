import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";
import {watch} from "vue";

export function onAuthenticated(callback: (data: {
  isAuthenticated: boolean
  isSuperuser: boolean
  isStaff: boolean
}) => void) {
  const mainStore = useMainStore();
  const {
    isAuthenticated,
    isSuperuser,
    isStaff,
  } = storeToRefs(mainStore)

  watch(isAuthenticated, () => {
      if (isAuthenticated.value) {
        callback({
          isAuthenticated: isAuthenticated.value,
          isSuperuser: isSuperuser.value,
          isStaff: isStaff.value,
        });
      }
  }, {
    immediate: true
  })
}
