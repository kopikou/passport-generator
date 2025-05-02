<script setup lang="ts">

import {computed, onBeforeMount, ref, watch, watchEffect} from "vue";
import {useQuasar} from "quasar";
import GeneratorAddPracticeDialog from "pages/generator/components/dialogs/GeneratorAddPracticeDialog.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {api} from "boot/axios";
import _ from "lodash";
import EmptyIcon from "components/EmptyIcon.vue";
import LayoutHCF from "components/LayoutHCF.vue";
import GeneratorDiscipline_Work_View from "pages/generator/components/GeneratorDiscipline_Work_View.vue";
import GeneratorDisciplineWorkViewBase from "pages/generator/components/GeneratorDisciplineWorkViewBase.vue";
import GeneratorDisciplineWorkHourContainer from "pages/generator/components/GeneratorDisciplineWorkHourContainer.vue";

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const {
  semestersData,
  practiceDisciplineWorkHour,
  rpdData,
  disciplineThemes,
  disabled,
  activeRpdId,
} = storeToRefs(generatorViewStore)
const tab = ref(0)

const allPercent = computed(() => {
  let hoursList = _.map(semestersData.value, (x) => x.pr)
  return _.sum(hoursList) || 0
})

const allPercentValue = computed(() => {
  let value = _.map(practiceDisciplineWorkHour.value, (x) => x.hours)
  return _.sum(value) || 0
})

const allSemesterPercent = computed(() => {
  let hoursList = _.map(_.filter(semestersData.value, (x) => tab.value == -1 ||  x.num == tab.value), (x) => x.pr)
  return _.sum(hoursList) || 0
})

const allSemesterPercentValue = computed(() => {
  let value = _.map(practiceDisciplineWorkHour.value, (x) => tab.value == -1 || x.semester == tab.value ? x.hours : 0)
  return _.sum(value) || 0
})

function addPractice() {
  $q.dialog({
    component: GeneratorAddPracticeDialog,
    componentProps: {
      sem: tab.value,
      id: null,
    },
  }).onOk(() => {
    generatorViewStore.checkErrors()
  })
}

function updatePractice(id) {
  $q.dialog({
    component: GeneratorAddPracticeDialog,
    componentProps: {
      sem: tab.value,
      id: id,
    },
  }).onOk(() => {
    generatorViewStore.checkErrors()
  })
}

function deletePractice(id) {
  $q.dialog({
    title: 'Удаление практического занятия',
    message: 'Вы точно хотите удалить практическое занятие?',
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

    $q.loading.show({message: "Удаление"})
    let r = await api.get(`/api/generator/${activeRpdId.value}/delete-discipline-work-hour/`, {params: {id: id}})

    rpdData.value.discipline_work_hour.splice(_.findKey(rpdData.value.discipline_work_hour, (x) => x.id == id), 1)
    generatorViewStore.checkErrors()
    $q.loading.hide()
  })
}

watchEffect(() => {
  tab.value = semestersData.value[0]?.num
})

const filteredData = computed(() => {
  return _.orderBy(practiceDisciplineWorkHour.value,  ['semester', 'num'])
})

async function fieldUp(num, sem) {
  let newKey = _.findKey(practiceDisciplineWorkHour.value, (x) => x.num == num - 1 && x.semester == sem)
  let oldKey = _.findKey(practiceDisciplineWorkHour.value, (x) => x.num == num && x.semester == sem)

  _.set(practiceDisciplineWorkHour.value, `[${oldKey}].num`, num - 1)
  _.set(practiceDisciplineWorkHour.value, `[${newKey}].num`, num)

  await saveData(_.get(practiceDisciplineWorkHour.value, `[${oldKey}]`))
  await saveData(_.get(practiceDisciplineWorkHour.value, `[${newKey}]`))
}

async function fieldDown(num, sem) {
  let newKey = _.findKey(practiceDisciplineWorkHour.value, (x) => x.num == num + 1 && x.semester == sem)
  let oldKey = _.findKey(practiceDisciplineWorkHour.value, (x) => x.num == num && x.semester == sem)

  _.set(practiceDisciplineWorkHour.value, `[${oldKey}].num`, num + 1)
  _.set(practiceDisciplineWorkHour.value, `[${newKey}].num`, num)

  await saveData(_.get(practiceDisciplineWorkHour.value, `[${oldKey}]`))
  await saveData(_.get(practiceDisciplineWorkHour.value, `[${newKey}]`))
}

async function saveData(data) {
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-discipline-work-hour/`, data)
  return r.data
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
    title="Перечень практических занятий по дисциплине"
    button-add-title="Добавить практическое занятие"
    @add-clicked="addPractice"
  >
    <template #content>
      <generator-discipline-work-hour-container
          :data="filteredData"
          v-model:sem="tab"
          @field-down="fieldDown"
          @field-up="fieldUp"
          @delete="deletePractice"
          @edit="updatePractice"
        />
    </template>
  </generator-discipline-work-view-base>
</template>

<style scoped lang="scss">
.practice-container {

  $border: 1px solid silver;

  > .practice-container__header {
    display: grid;
    grid-template-columns: 4% 1fr 15% 25% 10%  20%;
    font-weight: bold;
    border: $border;
    border-bottom: none;

    &:last-child {
      border-bottom: $border;
    }
  }

  > .practice-container__body {
    > .practice-container__body__cell {
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
