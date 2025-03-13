<script setup lang="ts">

import {onBeforeMount, ref, watch, computed} from "vue";
import {useQuasar} from "quasar";
import GeneratorAddIndependentDialog from "pages/generator/components/dialogs/GeneratorAddIndependentDialog.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";
import {api} from "boot/axios";
import EmptyIcon from "components/EmptyIcon.vue";

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const {
  semestersData,
  independentDisciplineWorkHour,
  rpdData,
  disciplineThemes,
  disabled,
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
  let hoursList = _.map(_.filter(semestersData.value, (x) => x.num == tab.value), (x) => x.srs)
  return _.sum(hoursList) || 0
})

const allSemesterPercentValue = computed(() => {
  let value = _.map(independentDisciplineWorkHour.value, (x) => x.semester == tab.value ? x.hours : 0)
  return _.sum(value) || 0
})

function addIndependent() {
  $q.dialog({
    component: GeneratorAddIndependentDialog,
    componentProps: {
      sem: tab.value,
      id: null,
    },
  })
}

function updateIndependent(id) {
  $q.dialog({
    component: GeneratorAddIndependentDialog,
    componentProps: {
      sem: tab.value,
      id: id,
    },
  })
}

function deleteIndependent(id) {
  $q.dialog({
    title: 'Удаление самостоятельного занятия',
    message: 'Вы точно хотите отправить самостоятельное занятие в архив?',
    ok: {
      label: 'В архив',
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
    let r = await api.get('api/generator/delete-discipline-work-hour/', {params: {id: id}})

    rpdData.value.discipline_work_hour.splice(_.findKey(rpdData.value.discipline_work_hour, (x) => x.id == id), 1)

    $q.loading.hide()
  })
}

watch(semestersData, () => {
  tab.value = `${semestersData.value[0].num}`
})

onBeforeMount(() => {
  tab.value = `${semestersData.value[0]?.num}`
})

const disciplineThemesByValue = computed(() => {
  return _.keyBy(disciplineThemes.value, 'id')
})

const maxNumberInSemester = computed(() => {
  let data = _.filter(independentDisciplineWorkHour.value, (x) => x.semester == tab.value)
  return _.max(_.map(data, (x) => x.num))
})

const filteredData = computed(() => {
  return _.orderBy(independentDisciplineWorkHour.value, (x) => x.theme_id, 'asc')
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
  let r = await api.post('api/generator/save-discipline-work-hour/', data)
  return r.data
}

function getRowColor(id) {
  let number = _.findKey(filteredData.value, x => x.id == id)
  return number % 2 == 0 ? 'bg-grey-3' : 'bg-white'
}

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Перечень самостоятельных работ по дисциплине</span>
      <p></p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div v-if="allPercent != 0">
        <q-btn label="Добавить новую самостоятельную работу" color="teal" class="q-mb-md" @click="addIndependent"
               :disabled="disabled"/>
        <q-linear-progress class="q-mb-md" size="20px" rounded :value="allPercentValue / allPercent" color="teal">
          <div class="absolute-full flex flex-center">
            <q-badge color="white" text-color="black" :label="`${allPercentValue} / ${allPercent}`"/>
          </div>
        </q-linear-progress>
        <q-tabs
          v-model="tab"
          align="left"
          narrow-indicator
          class="q-mb-md"
        >
          <q-tab class="text-teal bg-grey-4" v-for="item in semestersData" :name="`${item.num}`"
                 :label="`Семестр ${item.num}`"/>
        </q-tabs>
        <q-linear-progress class="q-mb-md" size="20px" rounded :value="allSemesterPercentValue / allSemesterPercent"
                           color="primary">
          <div class="absolute-full flex flex-center">
            <q-badge color="white" text-color="black" :label="`${allSemesterPercentValue} / ${allSemesterPercent}`"/>
          </div>
        </q-linear-progress>
        <q-tab-panels
          v-model="tab"
          animated
          transition-prev="scale"
          transition-next="scale"
        >
          <q-tab-panel v-for="item in semestersData" :name="`${item.num}`" class="independent-container">
            <div v-if="item" class="independent-container__header text-center text-subtitle1 items-center bg-grey-2">
              <!--              <div>-->
              <!--                Номер-->
              <!--              </div>-->
              <div>
                Вид самостоятельной работы
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
            <div v-for="independent in filteredData" class="independent-container__body">
              <div v-if="independent.semester == tab"
                   class="independent-container__body__cell text-subtitle1 text-center items-center"
                   :class="getRowColor(independent.id)">
<!--                                <div>-->
<!--                                  {{ independent.num }}-->
<!--                                </div>-->
                <div>
                  {{ independent.name }}
                </div>
                <div>
                  {{ independent.hours }}
                </div>
                <div>
                  {{ disciplineThemesByValue[independent.theme_id]?.num }}. {{ disciplineThemesByValue[independent.theme_id]?.name }}
                </div>
                <div v-show="!disabled">
                  <q-btn
                    icon="mdi-delete" color="red" flat @click="deleteIndependent(independent.id)"
                  />
                  <q-btn
                    icon="mdi-update" color="green" flat @click="updateIndependent(independent.id)"
                  />
<!--                  <q-btn v-if="independent.num != 1"-->
<!--                         icon="mdi-arrow-up-thin" color="black" flat :disabled="disabled"-->
<!--                         @click="fieldUp(independent.num, independent.semester)"-->
<!--                  />-->
<!--                  <q-btn v-if="independent.num != maxNumberInSemester"-->
<!--                         icon="mdi-arrow-down-thin" color="black" flat :disabled="disabled"-->
<!--                         @click="fieldDown(independent.num, independent.semester)"-->
<!--                  />-->
                </div>
              </div>
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </div>
      <div v-else>
        <p class="text-h6">Нет часов по самостоятельным занятиям</p>
        <empty-icon/>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.independent-container {

  $border: solid 1px silver;

  > .independent-container__header {
    display: grid;
    grid-template-columns: 1fr 15% 1fr 10%;
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
      grid-template-columns: 1fr 15% 1fr 10%;
      border: $border;
      border-bottom: none;

    }

    &:last-child {
      border-bottom: $border;
    }
  }
}
</style>
