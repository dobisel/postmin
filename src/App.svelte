<svelte:window on:popstate={e => softNavigate(e.state.target)} />
<Icons />

<!-- Initialization Overlay -->
{#if loading}
  <div class="loading all10">
    <p>Loading, please wait ... </p>
  </div>
{/if}

<!-- Navbar -->
<nav>
  <Logo {title}/>
  <NavItem bind:current title="Kitchen"  target="/kitchen"/>
  <NavItem bind:current title="Artists"  target="/kitchen"/>
  <NavItem bind:current title="Home"     target="/" />
</nav>
  
<div class="sm0 md0 lg1 xg2"></div>
<div class="sm10 md10 lg8 xg11 content">
  <!-- Content -->
  <svelte:component  
  this={route.component}
  bind:loading
  />
</div>
<div class="sm0 md0 lg1 xg2"></div>

<div class="all15 footer">
  <center>{ title } © 2021</center>
</div>
<style lang="sass" type="text/sass" global>
body
  height: 100%
  color: $fg
  background-color: $bg-verydark

nav
  background-color: $bg-dark
  width: 100%
  display: block
  height: $navheight
  border-style: inset
  border-bottom: 1px solid $bg-light
  padding-right: $gutter
  padding-left: $gutter

.content
  margin-top: $gutter * 4
  background: $bg-light

.loading
  position: absolute
  top: $navheight
  left: 0px
  width: 100%
  height: calc(100% - #{$navheight + $gutter})
  z-index: 80
  background: #000000
  text-align: center
  padding-top: $navheight * 3
  font-size: 2em

.footer p
  font-size: 0.6em

</style>
<script>
import { setContext } from 'svelte';
import Icons from './components/Icons.svelte';
import NavItem from './components/NavItem.svelte';
import Logo from './components/Logo.svelte';
import Home from './Home.svelte';
import Kitchen from './Kitchen.svelte';
import NotFound from './NotFound.svelte';

const routes = {
  '/':           {title: 'Home',       component: Home      },
  '/kitchen':    {title: 'Kitchen',    component: Kitchen   },
};

const notFound = {
  title: 'Not Found',
  component: NotFound,
};

let loading = true;
let route;
let current;
export let title;

/* Navigation */
function softNavigate(target) {
  current = target;
  route = routes[target];

  /* 404 */
  if (route == undefined) {
    route = notFound;
  }

  /* Set the page title */
  document.title = title;
  return false;
}


function navigate(target) {
  softNavigate(target);
  window.history.pushState({
    target
  }, 
    route.title, 
    `${window.location.origin}basePath${target}`
  );
}
setContext('nav', {navigate});

/* Match current route */
current = window.location.pathname.replace(new RegExp('^basePath'), '');
navigate(current);

</script>


