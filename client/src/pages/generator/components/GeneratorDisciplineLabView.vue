<script setup lang="ts">


import {useQuasar} from "quasar";
import {computed, onBeforeMount, ref, watch} from "vue";
import GeneratorAddLabDialog from "./dialogs/GeneratorAddLabDialog.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";
import {api} from "boot/axios";
import EmptyIcon from "components/EmptyIcon.vue";


const generatorViewStore = useGeneratorViewStore();

const {
  semestersData,
  labDisciplineWorkHour,
  disciplineThemes,
  rpdData,
  disabled,
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
  })
}

function updateLab(id) {
  $q.dialog({
    component: GeneratorAddLabDialog,
    componentProps: {
      sem: tab.value,
      id: id,
    },
  })
}

function deleteLab(id) {
  $q.dialog({
    title: 'Удаление лабораторного занятия',
    message: 'Вы точно хотите отправить лабораторное занятие в архив?',
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
    let r = await api.get('/api/generator/delete-discipline-work-hour/', {params: {id: id}})

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

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Перечень лабораторных работ по дисциплине</span>
      <p></p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div v-if="allPercent != 0">
        <q-btn label="Добавить новую лабораторную работу" color="teal" class="q-mb-md" @click="addLab" :disabled="disabled"/>
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
          <q-tab-panel v-for="item in semestersData" :name="`${item.num}`" class="lab-container">
            <div v-if="item" class="lab-container__header text-center text-subtitle1 items-center">
              <div>
                Номер
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
            <div v-for="lab in labDisciplineWorkHour" class="lab-container__body">
              <div v-if="lab.semester == tab"
                   class="lab-container__body__cell text-subtitle1 text-center items-center">
                <div>
                  {{ lab.num }}
                </div>
                <div>
                  {{ lab.name }}
                </div>
                <div>
                  {{ lab.hours }}
                </div>
                <div>
                  {{ disciplineThemesByValue[lab.theme_id]?.name }}
                </div>
                <div v-show="!disabled">
                  <q-btn
                    icon="mdi-delete" color="red" flat @click="deleteLab(lab.id)"
                  />
                  <q-btn
                    icon="mdi-update" color="green" flat @click="updateLab(lab.id)"
                  />
                </div>
              </div>
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </div>
      <div v-else>
        <p class="text-h6">Нет часов по лабораторным занятиям</p>
        <empty-icon/>
      </div>
    </div>
  </div>
</template>

<style scoped>

.lab-container {
  > .lab-container__header {
    display: grid;
    grid-template-columns: repeat(4, 1fr) auto;
    font-weight: bold;
  }

  > .lab-container__body {
    > .lab-container__body__cell {
      display: grid;
      grid-template-columns: repeat(4, 1fr) auto;
    }
  }
}

</style>
