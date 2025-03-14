<script setup lang="ts">
import {computed, nextTick, onBeforeMount, ref, watch} from "vue";
import {useQuasar} from "quasar";
import GeneratorDialogAddTheme from "pages/generator/components/dialogs/GeneratorAddThemeDialog.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _, {sumBy} from "lodash";
import {api} from "boot/axios";
import {moveArrayElement, useSortable} from "@vueuse/integrations/useSortable";


const $q = useQuasar()
const generatorViewStore = useGeneratorViewStore();

const {
  semestersData,
  disciplineThemes,
  formControl,
  rpdData,
  disabled,
} = storeToRefs(generatorViewStore)

const tab = ref(0)

function addTheme() {
  $q.dialog({
    component: GeneratorDialogAddTheme,
    componentProps: {
      sem: tab.value,
      id: null,
    },
  })
}

function updateTheme(id) {
  $q.dialog({
    component: GeneratorDialogAddTheme,
    componentProps: {
      sem: tab.value,
      id: id,
    },
  })
}

async function deleteTheme(id) {

  $q.dialog({
    title: 'Удаление темы',
    message: 'Вы точно хотите отправить тему в архив?',
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
    let r = await api.get(`/api/generator/delete-discipline-themes/`, {params: {id: id}})

    rpdData.value.discipline_themes.splice(_.findKey(disciplineThemes.value, (x) => x.id == id), 1)

    $q.loading.hide()
  })

}

const formControlByValue = computed(() => {
  return _.keyBy(formControl.value, 'id')
})

const maxNumberInSemester = computed(() => {
  let data = _.filter(disciplineThemes.value, (x) => x.semester == tab.value)
  return _.max(_.map(data, (x) => x.num))
})

const filteredData = computed(() => {
  return _.orderBy(disciplineThemes.value, (x) => x.num, 'asc')
})

async function fieldUp(num, sem) {
  let newKey = _.findKey(disciplineThemes.value, (x) => x.num == num - 1 && x.semester == sem)
  let oldKey = _.findKey(disciplineThemes.value, (x) => x.num == num && x.semester == sem)

  _.set(disciplineThemes.value, `[${oldKey}].num`, num - 1)
  _.set(disciplineThemes.value, `[${newKey}].num`, num)

  await saveThemeData(_.get(disciplineThemes.value, `[${oldKey}]`))
  await saveThemeData(_.get(disciplineThemes.value, `[${newKey}]`))
}

async function fieldDown(num, sem) {
  let newKey = _.findKey(disciplineThemes.value, (x) => x.num == num + 1 && x.semester == sem)
  let oldKey = _.findKey(disciplineThemes.value, (x) => x.num == num && x.semester == sem)

  _.set(disciplineThemes.value, `[${oldKey}].num`, num + 1)
  _.set(disciplineThemes.value, `[${newKey}].num`, num)

  await saveThemeData(_.get(disciplineThemes.value, `[${oldKey}]`))
  await saveThemeData(_.get(disciplineThemes.value, `[${newKey}]`))
}

async function saveThemeData(data) {
  let r = await api.post('/api/generator/save-discipline-themes/', data)
  return r.data
}

function getRowColor(number) {
  return number % 2 == 0 ? 'bg-grey-4' : 'bg-white'
}

watch(semestersData, () => {
  tab.value = `${semestersData.value[0].num}`
})

onBeforeMount(() => {
  tab.value = `${semestersData.value[0]?.num}`
})

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Содержание разделов и тем по дисциплине</span>
      <p></p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-btn label="Добавить тему дисциплины" color="teal" class="q-mb-md" @click="addTheme" :disabled="disabled"/>
      <q-tabs
        v-model="tab"
        align="left"
        narrow-indicator
        class="q-mb-md"
      >
        <q-tab class="text-teal bg-grey-4" v-for="item in semestersData" :name="`${item.num}`"
               :label="`Семестр ${item.num}`"/>
      </q-tabs>
      <q-tab-panels
        v-model="tab"
        animated
        transition-prev="scale"
        transition-next="scale"
      >
        <q-tab-panel v-for="item in semestersData" :name="`${item.num}`" class="theme-container">
          <div v-if="item" class="theme-container__header text-center text-subtitle1 items-center bg-grey-2">
            <div>
              №
            </div>
            <div>
              Наименование темы
            </div>
            <div>
              Форма контроля
            </div>
            <div>
              Краткое описание темы
            </div>
            <div>
              Управление
            </div>
          </div>
          <div v-for="item in filteredData" class="theme-container__body">
            <div v-if="item.semester == tab"
                 class="theme-container__body__cell text-subtitle1 text-center items-center"
                 :class="getRowColor(item.num)">
              <div>
                {{ item.num }}
              </div>
              <div>
                {{ item.name }}
              </div>
              <div>
                {{ formControlByValue[item.formcontrol_id]?.name }}
              </div>
              <div class="text-justify">
                {{ item.comment }}
              </div>
              <div>
                <q-btn
                  icon="mdi-delete" color="red" flat @click="deleteTheme(item.id)" :disabled="disabled"
                />
                <q-btn
                  icon="mdi-update" color="green" flat @click="updateTheme(item.id)" :disabled="disabled"
                />
                <q-btn v-if="item.num != 1"
                       icon="mdi-arrow-up-thin" color="black" flat :disabled="disabled"
                       @click="fieldUp(item.num, item.semester)"
                />
                <q-btn v-if="item.num != maxNumberInSemester"
                       icon="mdi-arrow-down-thin" color="black" flat :disabled="disabled"
                       @click="fieldDown(item.num, item.semester)"
                />
              </div>
            </div>
          </div>

        </q-tab-panel>
      </q-tab-panels>
    </div>
  </div>
</template>

<style scoped lang="scss">


.theme-container {

  $border: solid 1px silver;

  > .theme-container__header {
    display: grid;
    grid-template-columns: 4% 20% 15% 1fr 20%;
    font-weight: bold;
    border: $border;
    border-bottom: none;


    &:last-child {
      border-bottom: $border;
    }
  }

  > .theme-container__body {
    > .theme-container__body__cell {
      display: grid;
      grid-template-columns: 4% 20% 15% 1fr 20%;
      border: $border;
      border-bottom: none;

    }

    &:last-child {
      border-bottom: $border;
    }
  }
}


</style>
