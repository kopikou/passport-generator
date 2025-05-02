<script setup lang="ts">


import {useQuasar} from "quasar";
import {computed, onBeforeMount, ref, watch, watchEffect} from "vue";
import GeneratorAddLabDialog from "./dialogs/GeneratorAddLabDialog.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";
import {api} from "boot/axios";
import EmptyIcon from "components/EmptyIcon.vue";
import GeneratorDisciplineWorkViewBase from "pages/generator/components/GeneratorDisciplineWorkViewBase.vue";
import GeneratorDisciplineWorkHourContainer from "pages/generator/components/GeneratorDisciplineWorkHourContainer.vue";


const generatorViewStore = useGeneratorViewStore();

const {
  semestersData,
  labDisciplineWorkHour,
  disciplineThemes,
  rpdData,
  disabled,
  activeRpdId,
} = storeToRefs(generatorViewStore)

const $q = useQuasar()
const tab = ref(0)

const allPercent = computed(() => {
  let hoursList = _.map(semestersData.value, (x) => x.lab)
  return _.sum(hoursList) || 0
})

const allPercentValue = computed(() => {
  let value = _.map(labDisciplineWorkHour.value, (x) => x.hours)
  return _.sum(value) || 0
})

const allSemesterPercent = computed(() => {
  let hoursList = _.map(_.filter(semestersData.value, (x) => x.num == tab.value), (x) => x.lab)
  return _.sum(hoursList) || 0
})

const allSemesterPercentValue = computed(() => {
  let value = _.map(labDisciplineWorkHour.value, (x) => x.semester == tab.value ? x.hours : 0)
  return _.sum(value) || 0
})

function addLab() {
  $q.dialog({
    component: GeneratorAddLabDialog,
    componentProps: {
      sem: tab.value,
      id: null,
    },
  }).onOk(() => {
    generatorViewStore.checkErrors()
  })
}

function updateLab(id) {
  $q.dialog({
    component: GeneratorAddLabDialog,
    componentProps: {
      sem: tab.value,
      id: id,
    },
  }).onOk(() => {
    generatorViewStore.checkErrors()
  })
}

function deleteLab(id) {
  $q.dialog({
    title: 'Удаление лабораторной работы',
    message: 'Вы точно хотите удалить лабораторную работу?',
    ok: {
      label: 'Удалить',
      flat: true,
      color: 'red',
    },
    cancel: {
      label: 'Отмена',
      flat: true,
      color: 'green',
    },
    persistent: true
  }).onOk(async () => {

    // $q.loading.show({message: "Удаление"})
    let r = await api.get(`/api/generator/${activeRpdId.value}/delete-discipline-work-hour/`, {params: {id: id}})

    rpdData.value.discipline_work_hour.splice(_.findKey(rpdData.value.discipline_work_hour, (x) => x.id == id), 1)
    generatorViewStore.checkErrors()
    // $q.loading.hide()
  })
}

watchEffect(() => {
  tab.value = semestersData.value[0]?.num
})

const filteredData = computed(() => {
  return _.orderBy(labDisciplineWorkHour.value,  ['semester', 'num'])
})

async function saveData(data) {
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-discipline-work-hour/`, data)
  return r.data
}

async function fieldUp(num, sem) {
  let newKey = _.findKey(labDisciplineWorkHour.value, (x) => x.num == num - 1 && x.semester == sem)
  let oldKey = _.findKey(labDisciplineWorkHour.value, (x) => x.num == num && x.semester == sem)

  _.set(labDisciplineWorkHour.value, `[${oldKey}].num`, num - 1)
  _.set(labDisciplineWorkHour.value, `[${newKey}].num`, num)

  await saveData(_.get(labDisciplineWorkHour.value, `[${oldKey}]`))
  await saveData(_.get(labDisciplineWorkHour.value, `[${newKey}]`))
}

async function fieldDown(num, sem) {
  let newKey = _.findKey(labDisciplineWorkHour.value, (x) => x.num == num + 1 && x.semester == sem)
  let oldKey = _.findKey(labDisciplineWorkHour.value, (x) => x.num == num && x.semester == sem)

  _.set(labDisciplineWorkHour.value, `[${oldKey}].num`, num + 1)
  _.set(labDisciplineWorkHour.value, `[${newKey}].num`, num)

  await saveData(_.get(labDisciplineWorkHour.value, `[${oldKey}]`))
  await saveData(_.get(labDisciplineWorkHour.value, `[${newKey}]`))
}

</script>

<template>
  <generator-discipline-work-view-base
    :disabled="disabled"
    :all-percent="allPercent"
    :all-percent-value="allPercentValue"
    :all-semester-percent-value="allSemesterPercentValue"
    :all-semester-percent="allSemesterPercent"
    :semesters-data="semestersData"
    v-model:tab="tab"
    title="Перечень лабораторных работ по дисциплине"
    button-add-title="Добавить лабораторную работу"
    @add-clicked="addLab"
  >
    <template #content>
         <generator-discipline-work-hour-container
          :data="filteredData"
          v-model:sem="tab"
          @field-down="fieldDown"
          @field-up="fieldUp"
          @delete="deleteLab"
          @edit="updateLab"
        />
    </template>
  </generator-discipline-work-view-base>
</template>

<style scoped lang="scss">

.lab-container {

  $border: 1px solid silver;

  > .lab-container__header {
    display: grid;
    grid-template-columns: 4% 1fr 15% 25% 10%  20%;
    font-weight: bold;
    border: $border;
    border-bottom: none;

    &:last-child {
      border-bottom: $border;
    }
  }

  > .lab-container__body {
    > .lab-container__body__cell {
      display: grid;
      grid-template-columns: 4% 1fr 15% 25% 10%  20%;
      border: $border;
      border-bottom: none;

    }
      &:last-child {
        border-bottom: $border;
      }
  }
}

</style>
