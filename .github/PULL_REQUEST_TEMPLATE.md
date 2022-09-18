## The Checklist :see_no_evil: :hear_no_evil: :speak_no_evil:

### Type of the change:
###### (this is optional)
- [ ] :fire: Hotfix
- [ ] :rocket: "Big Deploy" (from develop / from preprod)

### The basics:
- [ ] <!--- required -->Review the commits and make sure they are aligned with what you are planning to merge.
- [ ] <!--- required -->Check that no weird commits “slipped” into the merge due to human error.
- [ ] <!--- required -->Go over briefly on the “File Changed” and make sure the files are aligned with what you expect.
- [ ] <!--- required -->Ensure that “All checks have passed”, that should include:
    - Build
    - Unit tests
    - Automated tests

### In case the version includes a new service:
###### (this is optional)
- [ ] Validate with the devops team that the new service is configured in preprod and prod environments (terraform, helm chart).

### In case this is a “big deploy” merge (from develop / from preprod):
###### (this is optional)
- [ ] In “Next Deploy” report all the deploy blockers have been marked as “Done” as needed.
- [ ] Validate the deploy to preprod with the same changes have been made and sanity tests have been performed.

### In case this is a “hotfix” merge:
###### (this is optional)
- [ ] Validate there is a PR merged in “develop” with the same changes.
- [ ] Validate the change was properly tested in “app-test”.
- [ ] The code was reviewed and approved.