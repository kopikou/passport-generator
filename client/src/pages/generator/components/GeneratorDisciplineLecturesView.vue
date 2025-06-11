<script setup lang="ts">

import {watchEffect, ref, watch, computed} from "vue";
import {useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import GeneratorAddLecturesDialog from "pages/generator/components/dialogs/GeneratorAddLecturesDialog.vue";
import _ from "lodash";
import {api} from "boot/axios";
import EmptyIcon from "components/EmptyIcon.vue";
import GeneratorDisciplineWorkViewBase from "pages/generator/components/GeneratorDisciplineWorkViewBase.vue";
import GeneratorDisciplineWorkHourContainer from "pages/generator/components/GeneratorDisciplineWorkHourContainer.vue";

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const {
  rpdData,
  semestersData,
  lecturesDisciplineWorkHour,
  disciplineThemes,
  disabled,
  activeRpdId,
} = storeToRefs(generatorViewStore)

const tab = ref(-1)

const allPercent = computed(() => {
  let hoursList = _.map(semestersData.value, (x) => x.lekc)
  return _.sum(hoursList) || 0
})

const allPercentValue = computed(() => {
  let value = _.map(lecturesDisciplineWorkHour.value, (x) => x.hours)
  return _.sum(value) || 0
})

const allSemesterPercent = computed(() => {
  let hoursList = _.map(_.filter(semestersData.value, (x) => tab.value == -1 || x.num == tab.value), (x) => x.lekc)
  return _.sum(hoursList) || 0
})

const allSemesterPercentValue = computed(() => {
  let value = _.map(lecturesDisciplineWorkHour.value, (x) => (tab.value == -1 || x.semester == tab.value) ? x.hours : 0)
  return _.sum(value) || 0
})

function addLectures() {
  $q.dialog({
    component: GeneratorAddLecturesDialog,
    componentProps: {
      sem: tab.value,
      id: null,
    },
  }).onOk(() => {
    generatorViewStore.checkErrors()
  })
}

function updateLectures(id) {
  $q.dialog({
    component: GeneratorAddLecturesDialog,
    componentProps: {
      sem: tab.value,
      id: id,
    },
  }).onOk(() => {
    generatorViewStore.checkErrors()
  })
}

function deleteLectures(id) {
  $q.dialog({
    title: 'Удаление лекционного занятия',
    message: 'Вы точно хотите удалить занятие?',
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


const filteredData = computed(() => {
  return _.orderBy(lecturesDisciplineWorkHour.value, ['semester', 'num'])
})


async function saveWorkHour(data) {
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-discipline-work-hour/`, data)
  return r.data
}

watchEffect(() => {
  tab.value = semestersData.value[0]?.num
})

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
    title="Перечень лекционных занятий по дисциплине"
    button-add-title="Добавить лекционное занятие"
    @add-clicked="addLectures"
  >
    <template #content>
      <generator-discipline-work-hour-container
        :data="filteredData"
        v-model:sem="tab"
        @delete="deleteLectures"
        @edit="updateLectures"
      />
    </template>
  </generator-discipline-work-view-base>
</template>

<style scoped lang="scss">


</style>
