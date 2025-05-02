<script setup lang="ts">

import {onBeforeMount, ref, watch, computed, watchEffect} from "vue";
import {useQuasar} from "quasar";
import GeneratorAddIndependentDialog from "pages/generator/components/dialogs/GeneratorAddIndependentDialog.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";
import {api} from "boot/axios";
import EmptyIcon from "components/EmptyIcon.vue";
import GeneratorDisciplineWorkViewBase from "pages/generator/components/GeneratorDisciplineWorkViewBase.vue";
import GeneratorDisciplineWorkHourContainer from "pages/generator/components/GeneratorDisciplineWorkHourContainer.vue";

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const {
  semestersData,
  independentDisciplineWorkHour,
  rpdData,
  disciplineThemes,
  disabled,
  activeRpdId,
} = storeToRefs(generatorViewStore)

const tab = ref(0)

const allPercent = computed(() => {
  let hoursList = _.map(semestersData.value, (x) => x.srs)
  return _.sum(hoursList) || 0
})

const allPercentValue = computed(() => {
  let value = _.map(independentDisciplineWorkHour.value, (x) => x.hours)
  return _.sum(value) || 0
})

const allSemesterPercent = computed(() => {
  let hoursList = _.map(_.filter(semestersData.value, (x) => tab.value == -1 || x.num == tab.value), (x) => x.srs)
  return _.sum(hoursList) || 0
})

const allSemesterPercentValue = computed(() => {
  let value = _.map(independentDisciplineWorkHour.value, (x) => tab.value == -1 ||  x.semester == tab.value ? x.hours : 0)
  return _.sum(value) || 0
})

function addIndependent() {
  $q.dialog({
    component: GeneratorAddIndependentDialog,
    componentProps: {
      sem: tab.value,
      id: null,
    },
  }).onOk(() => {
    generatorViewStore.checkErrors()
  })
}

function updateIndependent(id) {
  $q.dialog({
    component: GeneratorAddIndependentDialog,
    componentProps: {
      sem: tab.value,
      id: id,
    },
  }).onOk(() => {
    generatorViewStore.checkErrors()
  })
}

function deleteIndependent(id) {
  $q.dialog({
    title: 'Удаление самостоятельного занятия',
    message: 'Вы точно хотите удалить самостоятельное занятие?',
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

const disciplineThemesByValue = computed(() => {
  return _.keyBy(disciplineThemes.value, 'id')
})

const maxNumberInSemester = computed(() => {
  let data = _.filter(independentDisciplineWorkHour.value, (x) => x.semester == tab.value)
  return _.max(_.map(data, (x) => x.num))
})

const filteredData = computed(() => {
  return _.orderBy(independentDisciplineWorkHour.value,  ['semester', 'num'])
})

async function fieldUp(num, sem) {
  let newKey = _.findKey(independentDisciplineWorkHour.value, (x) => x.num == num - 1 && x.semester == sem)
  let oldKey = _.findKey(independentDisciplineWorkHour.value, (x) => x.num == num && x.semester == sem)

  _.set(independentDisciplineWorkHour.value, `[${oldKey}].num`, num - 1)
  _.set(independentDisciplineWorkHour.value, `[${newKey}].num`, num)

  await saveData(_.get(independentDisciplineWorkHour.value, `[${oldKey}]`))
  await saveData(_.get(independentDisciplineWorkHour.value, `[${newKey}]`))
}

async function fieldDown(num, sem) {
  let newKey = _.findKey(independentDisciplineWorkHour.value, (x) => x.num == num + 1 && x.semester == sem)
  let oldKey = _.findKey(independentDisciplineWorkHour.value, (x) => x.num == num && x.semester == sem)

  _.set(independentDisciplineWorkHour.value, `[${oldKey}].num`, num + 1)
  _.set(independentDisciplineWorkHour.value, `[${newKey}].num`, num)

  await saveData(_.get(independentDisciplineWorkHour.value, `[${oldKey}]`))
  await saveData(_.get(independentDisciplineWorkHour.value, `[${newKey}]`))
}

async function saveData(data) {
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-discipline-work-hour/`, data)
  return r.data
}

function getRowColor(id) {
  let number = _.findKey(filteredData.value, x => x.id == id)
  return number % 2 == 0 ? 'bg-grey-1' : 'bg-white'
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
    title="Перечень самостоятельных работ по дисциплине"
    button-add-title="Добавить новую самостоятельную работу"
    @add-clicked="addIndependent"
  >
    <template #content>
        <generator-discipline-work-hour-container
          :data="filteredData"
          v-model:sem="tab"
          @field-down="fieldDown"
          @field-up="fieldUp"
          @delete="deleteIndependent"
          @edit="updateIndependent"
        />
    </template>
  </generator-discipline-work-view-base>

</template>

<style scoped lang="scss">
.independent-container {

  $border: solid 1px silver;

  > .independent-container__header {
    display: grid;
    grid-template-columns: 1fr 15% 1fr 10% 10%;
    font-weight: bold;
    border: $border;
    border-bottom: none;

    &:last-child {
      border-bottom: $border;
    }
  }

  > .independent-container__body {
    > .independent-container__body__cell {
      display: grid;
      grid-template-columns: 1fr 15% 1fr 10%  10%;
      border: $border;
      border-bottom: none;

    }

    &:last-child {
      border-bottom: $border;
    }
  }
}
</style>
