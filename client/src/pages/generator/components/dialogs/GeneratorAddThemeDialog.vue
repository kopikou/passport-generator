<script setup lang="ts">

import {useDialogPluginComponent, useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import _ from "lodash";

const $q = useQuasar()
const generatorViewStore = useGeneratorViewStore();
const {
  formControl,
  rpdData,
  disciplineThemes,
  activeRpdId,
  semestersData,
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
    type: Number
  }
})

const themeName = ref('')
const control = ref([])
const comment = ref('')
const semNew = ref(0)
// const num = ref()

const correct = computed(() => {
  if (!themeName.value || themeName.value.length < 3) return true
  else if (!control.value) return true
  else if (!comment.value || comment.value.length < 10) return true
  // else if (!num.value || num.value <= 0) return true

  return false
})

async function onOKClick() {
  $q.loading.show({message: "Сохранение"})

  let maxNum = _.max(_(disciplineThemes.value)
      .filter((x) => x.semester == props.sem)
      .map((q) => q.num).value())

  if (!maxNum) maxNum = 1
  else maxNum += 1

  let data = _.keyBy(disciplineThemes.value, "id")

  let r = await api.post(`/api/generator/${activeRpdId.value}/save-discipline-themes/`, {
    planlineslink_id: rpdData.value.id,
    name: themeName.value,
    semester: semNew.value,
    formcontrol_list: control.value,
    comment: comment.value,
    id: props.id,
    num: props.id ? data[props.id].num : maxNum,
  })
  //
  // if (!props.id) {
  //   rpdData.value.discipline_themes.push(r.data)
  // } else {
  //   rpdData.value.discipline_themes[_.findKey(disciplineThemes.value, (x) => x.id == props.id)] = r.data
  // }

  $q.loading.hide()
  onDialogOK()
}

watch(() => props, () => {
  if (props.id) {
    let data = _.keyBy(disciplineThemes.value, "id")
    themeName.value = data[props.id].name
    control.value = data[props.id].formcontrol_list
    comment.value = data[props.id].comment
    semNew.value = data[props.id].semester
    // num.value = data[props.id].num
    } else {
    semNew.value = parseInt(props.sem);
  }
}, {
  immediate: true
})

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide" persistent>
    <q-card class="q-dialog-plugin" style="width: 700px;">
      <div class="q-pa-md q-gutter-md">
        <q-chip color="teal" class="text-subtitle1">Семестр {{ sem }}</q-chip>
        <q-input
          stack-label
          label="Название темы"
          v-model="themeName"
          filled
          :rules="[ val => val.length >= 4 || 'Введите больше 3-ех символов']"
          type="num"
        />
<!--        <q-input-->
<!--          stack-label-->
<!--          label="Номер"-->
<!--          v-model="num"-->
<!--          filled-->
<!--          :rules="[ val => val > 0 || 'Введите значение больше 0']"-->
<!--          type="number"-->
<!--        />-->
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
          multiple
          use-chips
        />
        <q-input
          stack-label
          label="Краткое описание темы"
          v-model="comment"
          filled
          :rules="[ val => val.length >= 11 || 'Введите больше 10-ти символов']"
          type="textarea"
        />
         <q-select
          stack-label
          label="Семестр"
          :options="semestersData"
          v-model="semNew"
          option-label="num"
          option-value="num"
          map-options
          emit-value
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
