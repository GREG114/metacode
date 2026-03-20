import { createRouter, createWebHistory } from 'vue-router'
import ModelList from '../views/ModelList.vue'
import ModelEdit from '../views/ModelEdit.vue'
import FormFill from '../views/FormFill.vue'
import FormDataList from '../views/FormDataList.vue'
import LayoutEditor from '../views/LayoutEditor.vue'

const routes = [
  {
    path: '/',
    redirect: '/models'
  },
  {
    path: '/models',
    name: 'ModelList',
    component: ModelList
  },
  {
    path: '/models/new',
    name: 'ModelNew',
    component: ModelEdit
  },
  {
    path: '/models/:id/edit',
    name: 'ModelEdit',
    component: ModelEdit,
    props: true
  },
  {
    path: '/forms/:modelId',
    name: 'FormFill',
    component: FormFill,
    props: true
  },
  {
    path: '/forms/:modelId/data',
    name: 'FormDataList',
    component: FormDataList,
    props: true
  },
  {
    path: '/layouts/:modelId',
    name: 'LayoutEditor',
    component: LayoutEditor,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router