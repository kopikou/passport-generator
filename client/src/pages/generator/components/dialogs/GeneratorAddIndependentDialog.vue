<script setup lang="ts">

import {useDialogPluginComponent, useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, ref, onBeforeMount} from "vue";
import _ from "lodash";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();

const{
  independentTypes,
  independentDisciplineWorkHour,
  rpdData,
  disciplineThemes,
}=storeToRefs(generatorViewStore)

defineEmits([
  ...useDialogPluginComponent.emits
])

const $q = useQuasar()
const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const props = defineProps({
  id: {
    required: true,
  },
  sem: {
    required: true,
  }
})

const name = ref()
const hourCount = ref(0)
const theme = ref()
// const num = ref()


const correct = computed(() => {
  if (!name.value || name.value.length < 3) return true
  else if (!hourCount.value || hourCount.value <= 0) return true
  else if (!theme.value) return true
  // else if (!num.value || num.value <= 0) return true

  return false
})

async function onOKClick() {
  $q.loading.show({message: "Сохранение"})
    let maxNum = _.max(_(independentDisciplineWorkHour.value)
      .filter((x) => x.semester == props.sem)
      .map((q) => q.num).value())

  if (!maxNum) maxNum = 1
  else maxNum += 1

  let r = await api.post('/api/generator/save-discipline-work-hour/', {
    planlineslink_id: rpdData.value.id,
    theme_id: theme.value,
    type: 2,  // Cамостоятельная
    name: name.value,
    hours: hourCount.value,
    semester: props.sem,
    id: props.id,
    num: maxNum,
  })

  if (!props.id) {
    rpdData.value.discipline_work_hour.push(r.data)
  } else {
    rpdData.value.discipline_work_hour[_.findKey(rpdData.value.discipline_work_hour, (x) => x.id == props.id)] = r.data
  }

  $q.loading.hide()
  onDialogOK()
}

onBeforeMount(() => {
  if (props.id) {
    let data = _.keyBy(independentDisciplineWorkHour.value, "id")
    name.value = data[props.id].name
    hourCount.value = data[props.id].hours
    theme.value = data[props.id].theme_id
    // num.value = data[props.id].num
  }
})

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide" persistent>
    <q-card class="q-dialog-plugin" style="width: 700px;">
      <div class="q-pa-md q-gutter-md">
        <q-chip color="teal" class="text-subtitle1">Семестр {{ sem }}</q-chip>
        <q-select
          stack-label
          label="Вид самостоятельной работы"
          filled
          :options="independentTypes"
          v-model="name"
          option-label="name"
          option-value="name"
          map-options
          emit-value
        />
<!--        <q-input-->
<!--          stack-label-->
<!--          label="Номер"-->
<!--          v-model="num"-->
<!--          filled-->
<!--          :rules="[ val => val > 0 || 'Введите значение больше 0']"-->
<!--          type="number"-->
<!--        />-->
        <q-input
            stack-label
            label="Количество часов"
            v-model="hourCount"
            filled
            type="number"
            :rules="[ val => val > 0 || 'Введите значение больше 0']"
        />
        <q-select
          stack-label
          label="Тема дисциплины"
          filled
          :options="disciplineThemes"
          v-model="theme"
          option-label="name"
          option-value="id"
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
