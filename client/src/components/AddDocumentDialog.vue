<script setup lang="ts">
import {useDialogPluginComponent} from "quasar";
import _ from "lodash";
import {computed, onBeforeMount, ref} from "vue";
import usePlanViewStore from "stores/planViewStore";
import {storeToRefs} from "pinia";
import {api} from "boot/axios";

const planViewStore = usePlanViewStore()
const {
  cafData,
  sync_option,
  documentsData,
  docTypes,
  planData,
} = storeToRefs(planViewStore);

defineEmits([
  ...useDialogPluginComponent.emits
])

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const name = ref('')
const type = ref(3)

const correct = computed(() => {
  if (type.value < 0 || type.value == 0) return true
  if (name.value.length < 3) return true

  return false
})

async function onOKClick() {
  let data = {name: name.value, type: 3, new_type_id: type.value, synchronize: true, plan_id: planData.value[0].id, manual: true}
  let r = await api.post('/api/plx/add-document-data/', data)
  documentsData.value.push(r.data.items)
  onDialogOK()
}

onBeforeMount(() => {
  name.value = ''
  type.value = 3
})

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <div class="q-pa-md q-gutter-md">
      <q-input
        label="Наименование документа"
        v-model="name"
        filled
        type="text"
        :rules="[
          val => !!val || 'Введите значение'
          ]"
      />

      <q-select
        label="Тип документа"
        type="number"
        emit-value
        map-options
        :options="docTypes"
        option-label="name"
        option-value="id"
        v-model="type"
        filled
      />
      </div>
      <q-card-actions align="right">
        <q-btn color="primary" label="Сохранить" @click="onOKClick" :disable="correct"/>
        <q-btn color="primary" label="Отмена" @click="onDialogCancel"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
