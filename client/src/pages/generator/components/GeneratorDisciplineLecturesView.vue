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

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const {
  rpdData,
  semestersData,
  lecturesDisciplineWorkHour,
  disciplineThemes,
  disabled,
} = storeToRefs(generatorViewStore)

const tab = ref(0)

const allPercent = computed(() => {
  let hoursList = _.map(semestersData.value, (x) => x.lekc)
  return _.sum(hoursList) || 0
})

const allPercentValue = computed(() => {
  let value = _.map(lecturesDisciplineWorkHour.value, (x) => x.hours)
  return _.sum(value) || 0
})

const allSemesterPercent = computed(() => {
  let hoursList = _.map(_.filter(semestersData.value, (x) => x.num == tab.value), (x) => x.lekc)
  return _.sum(hoursList) || 0
})

const allSemesterPercentValue = computed(() => {
  let value = _.map(lecturesDisciplineWorkHour.value, (x) => x.semester == tab.value ? x.hours : 0)
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
    let r = await api.get('/api/generator/delete-discipline-work-hour/', {params: {id: id}})

    rpdData.value.discipline_work_hour.splice(_.findKey(rpdData.value.discipline_work_hour, (x) => x.id == id), 1)
    generatorViewStore.checkErrors()
    $q.loading.hide()
  })
}

const disciplineThemesByValue = computed(() => {
  return _.keyBy(disciplineThemes.value, 'id')
})

const maxNumberInSemester = computed(() => {
  let data = _.filter(lecturesDisciplineWorkHour.value, (x) => x.semester == tab.value)
  return _.max(_.map(data, (x) => x.num))
})

const filteredData = computed(() => {
  return _.orderBy(lecturesDisciplineWorkHour.value, (x) => x.num, 'asc')
})

function getRowColor(number) {
  return number % 2 == 0 ? 'bg-grey-4' : 'bg-white'
}

async function saveWorkHour(data) {
  let r = await api.post('/api/generator/save-discipline-work-hour/', data)
  return r.data
}

async function fieldUp(num, sem) {
  let newKey = _.findKey(lecturesDisciplineWorkHour.value, (x) => x.num == num - 1 && x.semester == sem)
  let oldKey = _.findKey(lecturesDisciplineWorkHour.value, (x) => x.num == num && x.semester == sem)

  _.set(lecturesDisciplineWorkHour.value, `[${oldKey}].num`, num - 1)
  _.set(lecturesDisciplineWorkHour.value, `[${newKey}].num`, num)

  await saveWorkHour(_.get(lecturesDisciplineWorkHour.value, `[${oldKey}]`))
  await saveWorkHour(_.get(lecturesDisciplineWorkHour.value, `[${newKey}]`))
}

async function fieldDown(num, sem) {
  let newKey = _.findKey(lecturesDisciplineWorkHour.value, (x) => x.num == num + 1 && x.semester == sem)
  let oldKey = _.findKey(lecturesDisciplineWorkHour.value, (x) => x.num == num && x.semester == sem)

  _.set(lecturesDisciplineWorkHour.value, `[${oldKey}].num`, num + 1)
  _.set(lecturesDisciplineWorkHour.value, `[${newKey}].num`, num)

  await saveWorkHour(_.get(lecturesDisciplineWorkHour.value, `[${oldKey}]`))
  await saveWorkHour(_.get(lecturesDisciplineWorkHour.value, `[${newKey}]`))
}

watchEffect(() => {
  tab.value = `${semestersData.value[0]?.num}`
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
        <q-tab-panels
          v-model="tab"
          animated
          transition-prev="scale"
          transition-next="scale"
        >
          <q-tab-panel v-for="item in semestersData" :name="`${item.num}`" class="lectures-container">
            <div v-if="item" class="lectures-container__header text-center text-subtitle1 items-center bg-grey-2">
              <div>
                №
              </div>
              <div>
                Наименование лекционного занятия
              </div>
              <div>
                Количество часов
              </div>
              <div>
                Тема дисциплины
              </div>
              <div v-show="!disabled">
                Управление
              </div>
            </div>
            <div v-for="lectures in filteredData" class="lectures-container__body">
              <div v-if="lectures.semester == tab"
                   class="lectures-container__body__cell text-subtitle1 text-center items-center"
                   :class="getRowColor(lectures.num)">
                <div>
                  {{ lectures.num }}
                </div>
                <div class="text-justify">
                  {{ lectures.name }}
                </div>
                <div>
                  {{ lectures.hours }}
                </div>
                <div>
                  {{ disciplineThemesByValue[lectures.theme_id]?.num }}. {{ disciplineThemesByValue[lectures.theme_id]?.name }}
                </div>
                <div v-show="!disabled">
                  <q-btn
                    icon="mdi-delete" color="red" flat @click="deleteLectures(lectures.id)"
                  />
                  <q-btn
                    icon="mdi-update" color="green" flat @click="updateLectures(lectures.id)"
                  />
                  <q-btn v-if="lectures.num != 1"
                         icon="mdi-arrow-up-thin" color="black" flat :disabled="disabled"
                         @click="fieldUp(lectures.num, lectures.semester)"
                  />
                  <q-btn v-if="lectures.num != maxNumberInSemester"
                         icon="mdi-arrow-down-thin" color="black" flat :disabled="disabled"
                         @click="fieldDown(lectures.num, lectures.semester)"
                  />
                </div>
              </div>
            </div>
          </q-tab-panel>
        </q-tab-panels>
    </template>
  </generator-discipline-work-view-base>
</template>

<style scoped lang="scss">

.lectures-container {

  $border: solid 1px silver;

  > .lectures-container__header {
    display: grid;
    grid-template-columns: 4% 1fr 15% 25% 20%;
    font-weight: bold;
    border: $border;
    border-bottom: none;

    &:last-child {
      border-bottom: $border;
    }
  }

  > .lectures-container__body {
    > .lectures-container__body__cell {
      display: grid;
      grid-template-columns: 4% 1fr 15% 25% 20%;
      border: $border;
      border-bottom: none;

    }

    &:last-child {
      border-bottom: $border;
    }
  }
}

</style>
