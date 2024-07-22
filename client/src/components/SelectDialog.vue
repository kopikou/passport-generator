<script setup lang="ts">
import {useDialogPluginComponent} from "quasar";
import _ from "lodash";
import {computed, onBeforeMount, ref, watch} from "vue";
import usePlanViewStore from "stores/planViewStore";
import {storeToRefs} from "pinia";
import {api} from "boot/axios";


const props = defineProps({
  options: {
    type: Array
  },
})


const emit = defineEmits([
  'update:modelValue',
  ...useDialogPluginComponent.emits,
])

const value = ref(null)

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

async function onOKClick() {
  emit("update:modelValue", value.value)
  onDialogOK(value.value)
}

watch(() => props.modelValue,
  () => {
    value.value = props.modelValue;
  })

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <div class="q-pa-md q-gutter-md">

        <q-select
          :options="options"
          v-model="value"
          filled
          map-options
          emit-value
        >

        </q-select>

      </div>
      <q-card-actions align="right">
        <q-btn color="primary" label="OK" @click="onOKClick"/>
        <q-btn color="primary" label="Cancel" @click="onDialogCancel"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
