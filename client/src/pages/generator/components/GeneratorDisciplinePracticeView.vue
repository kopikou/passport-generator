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

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const {
  semestersData,
  practiceDisciplineWorkHour,
  rpdData,
  disciplineThemes,
  disabled,
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
  let hoursList = _.map(_.filter(semestersData.value, (x) => x.num == tab.value), (x) => x.pr)
  return _.sum(hoursList) || 0
})

const allSemesterPercentValue = computed(() => {
  let value = _.map(practiceDisciplineWorkHour.value, (x) => x.semester == tab.value ? x.hours : 0)
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
    let r = await api.get('/api/generator/delete-discipline-work-hour/', {params: {id: id}})

    rpdData.value.discipline_work_hour.splice(_.findKey(rpdData.value.discipline_work_hour, (x) => x.id == id), 1)
    generatorViewStore.checkErrors()
    $q.loading.hide()
  })
}

watchEffect(() => {
  tab.value = `${semestersData.value[0]?.num}`
})

const disciplineThemesByValue = computed(() => {
  return _.keyBy(disciplineThemes.value, 'id')
})

const maxNumberInSemester = computed(() => {
  let data = _.filter(practiceDisciplineWorkHour.value, (x) => x.semester == tab.value)
  return _.max(_.map(data, (x) => x.num))
})

const filteredData = computed(() => {
  return _.orderBy(practiceDisciplineWorkHour.value, (x) => x.num, 'asc')
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
  let r = await api.post('/api/generator/save-discipline-work-hour/', data)
  return r.data
}

function getRowColor(number) {
  return number % 2 == 0 ? 'bg-grey-3' : 'bg-white'
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
      <q-tab-panels
        v-model="tab"
        animated
        transition-prev="scale"
        transition-next="scale"
      >
        <q-tab-panel v-for="item in semestersData" :name="`${item.num}`" class="practice-container">
          <div v-if="item" class="practice-container__header text-center text-subtitle1 items-center bg-grey-2">
            <div>
              №
            </div>
            <div>
              Наименование практического занятия
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
          <div v-for="practice in filteredData" class="practice-container__body">
            <div v-if="practice.semester == tab"
                 class="practice-container__body__cell text-subtitle1 text-center items-center"
                 :class="getRowColor(practice.num)">
              <div>
                {{ practice.num }}
              </div>
              <div class="text-justify">
                {{ practice.name }}
              </div>
              <div>
                {{ practice.hours }}
              </div>
              <div>
                {{ disciplineThemesByValue[practice.theme_id]?.num }}.
                {{ disciplineThemesByValue[practice.theme_id]?.name }}
              </div>
              <div v-show="!disabled">
                <q-btn
                  icon="mdi-delete" color="red" flat @click="deletePractice(practice.id)"
                />
                <q-btn
                  icon="mdi-update" color="green" flat @click="updatePractice(practice.id)"
                />
                <q-btn v-if="practice.num != 1"
                       icon="mdi-arrow-up-thin" color="black" flat :disabled="disabled"
                       @click="fieldUp(practice.num, practice.semester)"
                />
                <q-btn v-if="practice.num != maxNumberInSemester"
                       icon="mdi-arrow-down-thin" color="black" flat :disabled="disabled"
                       @click="fieldDown(practice.num, practice.semester)"
                />
              </div>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
      <div v-if="allPercent == 0">
        <p class="text-h6">Нет часов по практическим занятиям</p>
        <empty-icon/>
      </div>
    </template>
  </generator-discipline-work-view-base>
</template>

<style scoped lang="scss">
.practice-container {

  $border: 1px solid silver;

  > .practice-container__header {
    display: grid;
    grid-template-columns: 4% 1fr 15% 25% 20%;
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
