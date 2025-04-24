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
  tab.value = `${semestersData.value[0]?.num}`
})

const maxNumberInSemester = computed(() => {
  let data = _.filter(labDisciplineWorkHour.value, (x) => x.semester == tab.value)
  return _.max(_.map(data, (x) => x.num))
})

const disciplineThemesByValue = computed(() => {
  return _.keyBy(disciplineThemes.value, 'id')
})

const filteredData = computed(() => {
  return _.orderBy(labDisciplineWorkHour.value, (x) => x.num, 'asc')
})

function getRowColor(number) {
  return number % 2 == 0 ? 'bg-grey-3' : 'bg-white'
}

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
        <q-tab-panels
          v-model="tab"
          animated
          transition-prev="scale"
          transition-next="scale"
        >
          <q-tab-panel v-for="item in semestersData" :name="`${item.num}`" class="lab-container">
            <div v-if="item" class="lab-container__header text-center text-subtitle1 items-center bg-grey-2">
                            <div>
                              №
                            </div>
              <div>
                Наименование лабораторной работы
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
            <div v-for="lab in filteredData" class="lab-container__body">
              <div v-if="lab.semester == tab"
                   class="lab-container__body__cell text-subtitle1 text-center items-center"
                   :class="getRowColor(lab.num)">
                                <div>
                                  {{ lab.num }}
                                </div>
                <div class="text-justify">
                  {{ lab.name }}
                </div>
                <div>
                  {{ lab.hours }}
                </div>
                <div>
                  {{ disciplineThemesByValue[lab.theme_id]?.num }}. {{ disciplineThemesByValue[lab.theme_id]?.name }}
                </div>
                <div v-show="!disabled">
                  <q-btn
                    icon="mdi-delete" color="red" flat @click="deleteLab(lab.id)"
                  />
                  <q-btn
                    icon="mdi-pencil-outline" color="green" flat @click="updateLab(lab.id)"
                  />
                  <q-btn v-if="lab.num != 1"
                         icon="mdi-arrow-up-thin" color="black" flat :disabled="disabled"
                         @click="fieldUp(lab.num, lab.semester)"
                  />
                  <q-btn v-if="lab.num != maxNumberInSemester"
                         icon="mdi-arrow-down-thin" color="black" flat :disabled="disabled"
                         @click="fieldDown(lab.num, lab.semester)"
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

.lab-container {

  $border: 1px solid silver;

  > .lab-container__header {
    display: grid;
    grid-template-columns: 4% 1fr 15% 25% 20%;
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
