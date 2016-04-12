# Generated from sensu-settings-1.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sensu-settings

Name:           rubygem-%{gem_name}
Version:        3.3.0
Release:        1%{?dist}
Summary:        The Sensu settings library, loader and validator
Group:          Development/Languages
License:        MIT
URL:            https://github.com/sensu/sensu-settings
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby
%if 0%{?fedora} > 21
BuildRequires:  rubygem(rspec2)
%else
BuildRequires:  rubygem(rspec)
%endif
BuildRequires:  rubygem(multi_json)

Requires:       rubygem(multi_json)

BuildArch: noarch
%if 0%{?rhel} > 0
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
The Sensu settings library, loader and validator.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_instdir}/{.gitignore,.travis.yml}


# Run the test suite
%check
pushd .%{gem_instdir}
sed -i /codeclimate-test-reporter/d spec/helpers.rb
sed -i /CodeClimate::TestReporter.start/d spec/helpers.rb

# Add missing symlinks, which break unit tests,
# see https://github.com/sensu/sensu-settings/issues/25
pushd ./spec/assets/conf.d
ln -s ../alternative/conf.d/ alternative
popd
pushd ./spec/assets/alternative/conf.d
ln -s ../conf.d loop
popd

%if 0%{?fedora} > 21
rspec2 -Ilib spec
%else
rspec -Ilib spec
%endif
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{gem_instdir}/LICENSE.txt
%{gem_instdir}/README.md
%{gem_instdir}/Gemfile

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/spec

%changelog
* Mon Feb 29 2016 Martin Mágr <mmagr@redhat.com> -  3.3.0-1
- Updated to upstream version 3.3.0

* Tue Jan 27 2015 Graeme Gillies <ggillies@redhat.com> - 1.2.0-1
- Initial package
