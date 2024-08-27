<script setup lang="ts">

import {useDialogPluginComponent, useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, onBeforeMount, ref} from "vue";
import {api} from "boot/axios";
import _ from "lodash";

const $q = useQuasar()
const generatorViewStore = useGeneratorViewStore();
const {
  formControl,
  rpdData,
  disciplineThemes,
} = storeToRefs(generatorViewStore)

defineEmits([
  ...useDialogPluginComponent.emits
])

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const props = defineProps({
  sem: {
    required: true,
  },
  id: {
    required: true,
  },
})

const themeName = ref('')
const control = ref()
const comment = ref('')

const correct = computed(() => {
  if (!themeName.value || themeName.value.length < 3) return true
  else if (!control.value || control.value == null) return true
  else if (!comment.value || comment.value.length < 10) return true

  return false
})

async function onOKClick() {
  $q.loading.show({message: "Сохранение"})
  let r = await api.post('/api/generator/save-discipline-themes/', {
    planlineslink_id: rpdData.value.id,
    name: themeName.value,
    semester: props.sem,
    formcontrol_id: control.value,
    comment: comment.value,
    id: props.id,
  })

  if (!props.id) {
    rpdData.value.discipline_themes.push(r.data)
  } else {
    rpdData.value.discipline_themes[_.findKey(disciplineThemes.value, (x) => x.id == props.id)] = r.data
  }

  $q.loading.hide()
  onDialogOK()
}

onBeforeMount(() => {
  if (props.id) {
    let data = _.keyBy(disciplineThemes.value, "id")
    themeName.value = data[props.id].name
    control.value = data[props.id].formcontrol_id
    comment.value = data[props.id].comment
  }
})

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin" style="width: 700px;">
      <div class="q-pa-md q-gutter-md">
        <q-chip color="teal" class="text-subtitle1">Семестр {{ sem }}</q-chip>
        <q-input
            stack-label
            label="Название темы"
            v-model="themeName"
            filled
            :rules="[ val => val.length >= 4 || 'Введите больше 3-ех символов']"
            type="textarea"
        />
        <q-select
            stack-label
            label="Форма контроля"
            filled
            :options="formControl"
            v-model="control"
            option-label="name"
            option-value="id"
            map-options
            emit-value
        />
        <q-input
            stack-label
            label="Краткое описание темы"
            v-model="comment"
            filled
            :rules="[ val => val.length >= 11 || 'Введите больше 10-ти символов']"
            type="textarea"
        />
      </div>
      <q-card-actions align="right">
        <q-btn flat color="teal" label="Сохранить" @click="onOKClick" :disabled="correct"/>
        <q-btn flat color="red" label="Отмена" @click="onDialogCancel"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
